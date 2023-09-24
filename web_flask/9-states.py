#!/usr/bin/python3
"""a script that starts a web flask application to display
html data from the db"""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route('/states', strcit_slashes=False)
def states():
    states = storage.all('State')
    return render_template('9-states.html', state=states)


@app.route('/states/<id>', strict_slashes=False)
def states_id():
    for states in storage.all('State').values():
        if state.id == id:
            return render_template('9-states.html', state=states)
    return render_template('9-states.html')


@app.teardown_appcontext
def teardown(exc):
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
