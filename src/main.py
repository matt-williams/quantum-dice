import requests
from random import randint
from hashlib import sha256
from flask import Flask
from sense_hat import SenseHat
import threading

app = Flask(__name__)
sense = SenseHat()
sense.clear()
sense.set_rotation(90, False)

# SenseHat display
black = [0, 0, 0]
red = [255, 0, 0]
blue = [0, 0, 255]

def error(_, x):
    return [
    x, x, x, x, x, x, x, x,
    x, x, x, x, x, x, x, x,
    x, x, x, x, x, x, x, x,
    x, x, x, x, x, x, x, x,
    x, x, x, x, x, x, x, x,
    x, x, x, x, x, x, x, x,
    x, x, x, x, x, x, x, x,
    x, x, x, x, x, x, x, x
    ]

def six(_, x):
    return [
    x, x, _, _, _, _, x, x,
    x, x, _, _, _, _, x, x,
    _, _, _, _, _, _, _, _,
    x, x, _, _, _, _, x, x,
    x, x, _, _, _, _, x, x,
    _, _, _, _, _, _, _, _,
    x, x, _, _, _, _, x, x,
    x, x, _, _, _, _, x, x
    ]

def five(_, x):
    return [
    x, x, _, _, _, _, x, x,
    x, x, _, _, _, _, x, x,
    _, _, _, _, _, _, _, _,
    _, _, _, x, x, _, _, _,
    _, _, _, x, x, _, _, _,
    _, _, _, _, _, _, _, _,
    x, x, _, _, _, _, x, x,
    x, x, _, _, _, _, x, x
    ]

def four(_, x):
    return [
    x, x, _, _, _, _, x, x,
    x, x, _, _, _, _, x, x,
    _, _, _, _, _, _, _, _,
    _, _, _, _, _, _, _, _,
    _, _, _, _, _, _, _, _,
    _, _, _, _, _, _, _, _,
    x, x, _, _, _, _, x, x,
    x, x, _, _, _, _, x, x
    ]

def three(_, x):
    return [
    x, x, _, _, _, _, _, _,
    x, x, _, _, _, _, _, _,
    _, _, _, _, _, _, _, _,
    _, _, _, x, x, _, _, _,
    _, _, _, x, x, _, _, _,
    _, _, _, _, _, _, _, _,
    _, _, _, _, _, _, x, x,
    _, _, _, _, _, _, x, x
    ]

def two(_, x):
    return [
    x, x, _, _, _, _, _, _,
    x, x, _, _, _, _, _, _,
    _, _, _, _, _, _, _, _,
    _, _, _, _, _, _, _, _,
    _, _, _, _, _, _, _, _,
    _, _, _, _, _, _, _, _,
    _, _, _, _, _, _, x, x,
    _, _, _, _, _, _, x, x
    ]

def one(_, x):
    return [
    _, _, _, _, _, _, _, _,
    _, _, _, _, _, _, _, _,
    _, _, _, _, _, _, _, _,
    _, _, _, x, x, _, _, _,
    _, _, _, x, x, _, _, _,
    _, _, _, _, _, _, _, _,
    _, _, _, _, _, _, _, _,
    _, _, _, _, _, _, _, _
    ]

# Roll dice
def roll():
    print( 'In roll()' )
    own_diceroll = randint( 0, 1000 )
    print( 'own dice roll: %d' %( own_diceroll, ) )
    roll = own_diceroll % 6 + 1
    print( 'roll: %d' %( roll, ) )
    display( roll, False )
    return own_diceroll

# Sends a POST request to /start with hash of own dice roll value as a parameter
def start( diceroll ):
    print( 'In start()' )
    print( str( diceroll ) )
    h = hashlib.sha256()
    print( 'Initialised h' )
    # print( diceroll )
    h.update( "abs" )
    print( 'Updated h')
    hash = h.hexdigest()
    print( 'Assigned %s to hash' %( hash, ) )
    # h = sha256( '%d' %( diceroll, ) ).hexdigest()
    # print( 'hash: %d' %( h, ) )
    j = "{ 'hash': h }"
    print( 'json: %s' %( j, ) )
    r = requests.post( 'https://6074bef5efb0b8470f971bc524900c8e986040f9e4382942f6231162557d08.resindevice.io/start', json=j )
    # r.json should contain the other diceroll and its hash
    print( 'r.json: %s' %( r.json, ) )
    # display( combine( diceroll, r.json['diceroll'] ), True )
    sense.show_message('Confused')

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
            x = blue
        else:
            x = red
        sense.set_pixels( int_mod6_to_string( diceroll, black, x) )

# Displays error
def display_error():
    sense.set_pixels( error(black, red) )

# Converts an int dice roll into a string for display
def int_mod6_to_string(value, _, x):
    return {
        1 : one,
        2 : two,
        3 : three,
        4 : four,
        5 : five,
        6 : six
    } [value](_, x)

@app.route('/')
def hello_world():
    sense.show_message("Hello world!")
    return 'Hello World!'

@app.route('/roll')
def get_roll():
    print( 'In get_roll()' )
    start( roll() )
    return 'ROLL'

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

