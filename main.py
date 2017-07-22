#!/usr/bin/env python
"""Operate list of tasks."""

from boto.dynamodb2.fields import HashKey
from boto.dynamodb2.table import Table

from flask import Flask
from flask.ext.autodoc import Autodoc
from flask.ext.dynamo import Dynamo
from task.task import Task

app = Flask(__name__)
auto = Autodoc(app)
app.config['DYNAMO_TABLES'] = [
    Table('tasks_master', schema=[HashKey('id')]),
]

dynamo = Dynamo(app)


@app.route('/init', methods=["GET"])
@auto.doc()
def init():
    """Initialize database tables."""
    with app.app_context():
        dynamo.create_all()

    resp = list()

    with app.app_context():
        for table_name, table in dynamo.tables.iteritems():
            resp.append(str((table_name, table)))

    return "\n".join(resp)


@app.route('/task/list', methods=["GET"])
@app.route('/', methods=["GET"])
@auto.doc()
def index():
    """Return list of open tasks."""
    return "Hello World!"


@app.route('/task/create', methods=["GET", "POST"])
@auto.doc()
def task_create():
    """Add new task to a list."""
    task = Task()
    dynamo.tasks_master.put_item(data={
        'id': task.get_id(),
        'first_name': 'Randall',
        'last_name': 'Degges',
        'email': 'r@rdegges.com',
    })
    return "Task ID: %s" % task.get_id()


@app.route('/task/destroy/<string:task_id>', methods=["GET"])
@auto.doc()
def task_destroy(task_id):
    """Add new task to a list."""
    pass


@app.route('/help', methods=["GET"])
@auto.doc()
def docs():
    """Return API documentation."""
    return auto.html()


if __name__ == '__main__':
    app.run()
