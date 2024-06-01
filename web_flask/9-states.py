#!/usr/bin/python3
""" A script that starts a web app using storage for fetching data from engine
Routes:
    /states: display a HTML page inside tag BODY
    H1: States
    UL: with the list of all State objects in present DB sorted by name
        LI: description of one State: <state.id>: <B><state.name><B>

    /states/<id>: display a HTML page inside the tag BODY
    if a State object is found with this id:
        H1: State
        H3: Cities
        UL: with the list of City objects linked to State sorted by name
            LI: description of one City: <city.id>: <B><city.name></B>
        Otherwise:
            H1: Not found
"""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route("/states", strict_slashes=False)
def states():
    """ Returns an HTML page of all States sorted by name """
    states = storage.all(State)
    return render_template('9-states.html', states=states)


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """Displays a HTML page with info about <id>, if it exists."""
    for state in storage.all(State).values():
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")


@app.teardown_appcontext
def teardown_appcontext(exception):
    """ Removes the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
