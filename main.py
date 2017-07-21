#!/usr/bin/env python

from flask import Flask
from flask.ext.autodoc import Autodoc


app = Flask(__name__)
auto = Autodoc(app)


@app.route('/', methods=["GET"])
@auto.doc()
def index():
    """Return list of open tasks."""
    return "Hello World!"


@app.route('/help', methods=["GET"])
@auto.doc()
def docs():
    """Return API documentation."""
    return auto.html()


if __name__ == '__main__':
    app.run()
