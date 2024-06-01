#!/usr/bin/python3
""" A script that starts a flask web app listening on 0.0.0.0, port 5000
Routes:
    /: display "Hello HBNB!"
    /hbnb: display "HBNB"
    /c/<text>: display C followed by value of text variable
    /python/<text>: display Python followed by value of text variable
    value of text is "is cool".
    /number/<n>: display "n is a number" only if n is an integer
    /number_template/<n>: display a HTML page only if n is an int:
        H1 tag: "Number: n" inside the tag BODY
"""
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_HBNB():
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    return 'HBNB'


# New dynamic route
@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """ Replace underscores with spaces in the text"""
    display_text = text.replace('_', ' ')
    return 'C {}'.format(display_text)


# New route for /python/<text> with default value "is cool"
@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text="is cool"):
    display_text = text.replace('_', ' ')
    return 'Python {}'.format(display_text)


# New route for /number/<n> that displays only if n is an int
@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    return '{} is a number'.format(n)


# new route that displays html file using the render_template
@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """Returns an HTML page only if n is an int"""
    return render_template('5-number.html', n=n)


if __name__ == "__main__":
    # çonfigure the app to listen on 0.0.0.0, port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
