#!/usr/bin/env python
"""Operate list of tasks."""

from boto.dynamodb2.fields import HashKey, RangeKey, GlobalAllIndex
from boto.dynamodb2.table import Table
from boto.dynamodb2.types import NUMBER
from botocore.exceptions import ClientError

from flask import Flask, abort, request
from flask_autodoc import Autodoc
from flask_dynamo import Dynamo
from task.task import Task

import json
import decimal

app = Flask(__name__)
auto = Autodoc(app)
app.config['DYNAMO_TABLES'] = [
    Table(
        'tasks_master',
        schema=[
            HashKey('id'),
            RangeKey('timestamp', data_type=NUMBER)
        ],
        global_indexes=[
            GlobalAllIndex('secondKeyIndex', parts=[
                HashKey('owner')
            ])
        ],
        throughput={'read': 1, 'write': 1}
    )
    ]

dynamo = Dynamo(app)


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


@app.route('/init', methods=["GET"])
@auto.doc()
def init():
    """Initialize database tables."""
    with app.app_context():
        dynamo.create_all()

    data = {"tables": []}
    with app.app_context():
        for table_name, table in dynamo.tables.iteritems():
            data["tables"].append(str((table_name, table)))

    return json.dumps(data, indent=4, cls=DecimalEncoder)


@app.route('/', methods=["GET"])
@app.route('/task/list', methods=["GET"])
@auto.doc()
def index():
    """Return list of open tasks."""
    data = {"items": []}
    length = 0

    data["table_name"] = "tasks_master"
    results = dynamo.tasks_master.scan()
    for r in results:
        data["items"].append(dict(r.items()))
        length += 1
    data["items_length"] = length

    return json.dumps(data, indent=4, cls=DecimalEncoder)


@app.route('/task/create', methods=["GET", "POST"])
@auto.doc()
def task_create():
    """Add new task to a list."""
    task = Task(None)

    if request.method == "POST":
        content = request.get_json(silent=True)
        if not content:
            abort(400)
        task.from_dict(content)

    dynamo.tasks_master.put_item(data=task.as_dict())
    return "Task ID: %s" % task.get_id()


@app.route('/task/destroy/<string:task_id>', methods=["GET", "DELETE"])
@auto.doc()
def task_destroy(task_id):
    """Add new task to a list."""
    data = {"deleted_keys": []}
    results_length = 0

    try:
        results = dynamo.tasks_master.query(id__eq=task_id)
        for r in results:
            data["deleted_keys"].append(dict(r.items()))
            r.delete()
            results_length += 1
        if results_length < 1:
            abort(404)
    except ClientError as e:
        abort(500)
    return json.dumps(data, indent=4, cls=DecimalEncoder)


@app.route('/task/search/<string:owner>', methods=["GET"])
@auto.doc()
def task_search(owner):
    """Return list of Tasks wit specified owner."""
    data = {"items": []}
    length = 0

    data["table_name"] = "tasks_master"
    results = dynamo.tasks_master.query(owner__eq=owner,
                                        index='secondKeyIndex')
    for r in results:
        data["items"].append(dict(r.items()))

        t = Task("")
        t.from_dict(dict(r.items()))
        length += 1
    data["items_length"] = length

    if length < 1:
        abort(404)

    return json.dumps(data, indent=4, cls=DecimalEncoder)


@app.route('/debug', methods=["GET"])
@auto.doc()
def debug():
    """Start internal debugger (console only)."""
    import pdb

    table = dynamo.tasks_master
    pdb.set_trace()
    return "Hello world!"


@app.route('/help', methods=["GET"])
@auto.doc()
def docs():
    """Return API documentation."""
    return auto.html()


if __name__ == '__main__':
    app.run()
