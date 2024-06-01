#!/usr/bin/python3
""" A script that starts a web app using storage for fetching data from engine
Routes:
    /states_list: display a HTML page inside tag BODY
    H1: States
    UL: with the list of all State objects in present DB
        LI: description of one State: <state.id>: <B><state.name><B>
"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """ Returns an HTML page of all States sorted by name """
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """ Removes the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
