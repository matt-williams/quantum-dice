import requests
import sys
from random import randint
from flask import Flask
from sense_hat import SenseHat
import threading

app = Flask(__name__)
sense = SenseHat()

# SenseHat display
O = [0, 0, 0]
red = [255, 0, 0]
blue = [0, 0, 255]

def error(O, X):
    return [
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X,
    X, X, X, X, X, X, X, X
    ]

def six(O, X):
    return [
    X, X, O, X, X, O, X, X,
    X, X, O, X, X, O, X, X,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    X, X, O, X, X, O, X, X,
    X, X, O, X, X, O, X, X
    ]

def five(O, X):
    return [
    X, X, O, O, O, O, X, X,
    X, X, O, O, O, O, X, X,
    O, O, O, O, O, O, O, O,
    O, O, O, X, X, O, O, O,
    O, O, O, X, X, O, O, O,
    O, O, O, O, O, O, O, O,
    X, X, O, O, O, O, X, X,
    X, X, O, O, O, O, X, X
    ]

def four(O, X):
    return [
    X, X, O, O, O, O, X, X,
    X, X, O, O, O, O, X, X,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    X, X, O, O, O, O, X, X,
    X, X, O, O, O, O, X, X
    ]

def three(O, X):
    return [
    X, X, O, O, O, O, O, O,
    X, X, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, X, X, O, O, O,
    O, O, O, X, X, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, X, X,
    O, O, O, O, O, O, X, X
    ]

def two(O, X):
    return [
    X, X, O, O, O, O, O, O,
    X, X, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, X, X,
    O, O, O, O, O, O, X, X
    ]

def one(O, X):
    return [
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, X, X, O, O, O,
    O, O, O, X, X, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O
    ]

# Roll dice
def roll():
    own_diceroll = randint( -maxint - 1, maxint )
    logging.info( 'dice roll: ' + own_diceroll )
    display( diceroll % 6 + 1, False )

# Sends a GET request with own dice roll value as a parameter
def send( diceroll ):
    r = requests.get('http:#0.0.0.0:80/combine', params=diceroll)
    logging.info( 'r.text: ' + r.text )
    display( combine( diceroll, r.text ), True )

# Computes the combined dice roll
def combine( own, other ):
    return ( ( own + other ) % 6 + 1)

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
        sense.set_pixels( int_mod6_to_string( diceroll, O, X) )

# Displays error
def display_error():
    sense.set_pixels( error(O, red) )

# Converts an int dice roll into a string for display
def int_mod6_to_string(value, O, X):
    return {
        1 : one,
        2 : two,
        3 : three,
        4 : four,
        5 : five,
        6 : six
    } [value](O, X)

@app.route('/')
def hello_world():
    sense.show_message("Hello world!")
    return 'Hello World!'

@app.route('/roll')
def get_roll():
    roll()

@app.route('/combine')
def get_combine():
    sense.show_message("Combine")

sense.set_imu_config(False, True, False) 
old_acc = sense.get_accelerometer_raw()
def poll_sensors():
    global old_acc
    acc = sense.get_accelerometer_raw()
    acc_delta = {'x': acc['x'] - old_acc['x'], 'y': acc['y'] - old_acc['y'], 'z': acc['z'] - old_acc['z']}
    if abs(acc_delta['x']) > 0.1 or abs(acc_delta['y']) > 0.1 or abs(acc_delta['z']) > 0.1:
        print(acc)
        display(randint(1, 6), False)
    old_acc = acc
    threading.Timer(0.01, poll_sensors, ()).start()

if __name__ == '__main__':
    poll_sensors()
    app.run(host='0.0.0.0', port=80)

