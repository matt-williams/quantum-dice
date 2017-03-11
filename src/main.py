import requests
import sys
from random import randint
from flask import Flask
from sense_hat import SenseHat

app = Flask(__name__)
sense = SenseHat()

@app.route('/')
def hello_world():
    sense.show_message("Hello world!")
    return 'Hello World!'

@app.get('/roll')
def get_roll():
    roll()

@app.get('/combine')
def get_combine():
    sense.show_message("Combine")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

# Roll dice
def roll():
    own_diceroll = randint( -maxint - 1, maxint )
    logging.info( 'dice roll: ' + own_diceroll )
    display( diceroll % 6, false )

# Sends a GET request with own dice roll value as a parameter
def send( diceroll ):
    r = requests.get('http:#0.0.0.0:80/combine', params=diceroll)
    logging.info( 'r.text: ' + r.text )
    display( combine( diceroll, r.text ), true )

# Computes the combined dice roll
def combine( own, other ):
    return ( ( own + other ) % 6 )

# Displays diceroll: own - red, combined - blue
def display( diceroll, isCombined ):
    if( diceroll < 1 or diceroll > 6 ):
        logging.debug( 'Dice roll is not between 1 and 6' )
        display_error()
    else:
        if( isCombined ):
            X = blue
        else:
            X = red
        sense.set_pixels( int_mod6_to_string( diceroll) )

# Displays error
def display_error():
    X = red
    sense.set_pixels( error )

# Converts an int dice roll into a string for display
def int_mod6_to_string( int ):
    return {
        0 : 'one',
        1 : 'two',
        2 : 'three',
        3 : 'four',
        4 : 'five',
        5 : 'six'
    } [ int ]

# SenseHat display
O = [255, 255, 255]
red = [255, 0, 0]
blue = [0, 0, 255]

error = [
X, X, X, X, X, X, X, X,
X, X, X, X, X, X, X, X,
X, X, X, X, X, X, X, X,
X, X, X, X, X, X, X, X,
X, X, X, X, X, X, X, X,
X, X, X, X, X, X, X, X,
X, X, X, X, X, X, X, X,
X, X, X, X, X, X, X, X
]

six = [
X, X, O, X, X, O, X, X,
X, X, O, X, X, O, X, X,
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O,
X, X, O, X, X, O, X, X,
X, X, O, X, X, O, X, X
]

five = [
X, X, O, O, O, O, X, X,
X, X, O, O, O, O, X, X,
O, O, O, O, O, O, O, O,
O, O, O, X, X, O, O, O,
O, O, O, X, X, O, O, O,
O, O, O, O, O, O, O, O,
X, X, O, O, O, O, X, X,
X, X, O, O, O, O, X, X
]

four = [
X, X, O, O, O, O, X, X,
X, X, O, O, O, O, X, X,
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O,
X, X, O, O, O, O, X, X,
X, X, O, O, O, O, X, X
]

three = [
X, X, O, O, O, O, O, O,
X, X, O, O, O, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, X, X, O, O, O,
O, O, O, X, X, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, X, X,
O, O, O, O, O, O, X, X
]

two = [
X, X, O, O, O, O, O, O,
X, X, O, O, O, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, X, X,
O, O, O, O, O, O, X, X
]

one = [
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, X, X, O, O, O,
O, O, O, X, X, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O
]
