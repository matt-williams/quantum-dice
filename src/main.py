import requests
import sys
import os
import json
from random import randint
from hashlib import sha256
from flask import Flask
from sense_hat import SenseHat
import threading

device_uuid = os.environ['RESIN_DEVICE_UUID']
peer_device_uuid = {
    '6074bef5efb0b8470f971bc524900c8e986040f9e4382942f6231162557d08': '5aa4169d9d408523669f4c05a5799f423809d947245aa52a91346a5fc3387a',
    '5aa4169d9d408523669f4c05a5799f423809d947245aa52a91346a5fc3387a': '6074bef5efb0b8470f971bc524900c8e986040f9e4382942f6231162557d08'
}[device_uuid]

app = Flask(__name__)
sense = SenseHat()
sense.clear()
sense.set_rotation(90, False)

# SenseHat display
black = [0, 0, 0]
red = [255, 0, 0]
green = [0, 255, 0]
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
    return own_diceroll

# Sends a POST request to /start with hash of own dice roll value as a parameter
def start( diceroll ):
    print( 'In start()' )
    print( str( diceroll ) )
    h = sha256()
    print( 'Initialised h' )
    h.update(str(diceroll).encode("UTF-8"))
    print( 'Updated h')
    hash = h.hexdigest()
    print( 'Assigned %s to hash' %( hash, ) )
    j = json.dumps( { 'hash': diceroll } )
    print( 'json: %s' %( j, ) )
    r = requests.post( 'https://%s.resindevice.io/respond' % (peer_device_uuid,), json=j )

# When receiving a POST request to /start
def respond():
   print( 'In respond()' )
   j = request.json
   print( j )
   # other_diceroll = json. 

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
        display_dice(diceroll, x)

def display_dice(value, x):
    sense.set_pixels(int_mod6_to_string(value, black, x))

# Displays error
def display_error():
    sense.set_pixels( error(black, red) )

def merge(img1, img2, alpha):
    return [[int(alpha * img1[ii][0] + (1 - alpha) * img2[ii][0]), int(alpha * img1[ii][1] + (1 - alpha) * img2[ii][1]), int(alpha * img1[ii][2] + (1 - alpha) * img2[ii][2])] for ii in range(min(len(img1), len(img2)))]

# Converts an int dice roll into a string for display
def int_mod6_to_string(value, _, x):
    return {
        1 : one,
        2 : two,
        3 : three,
        4 : four,
        5 : five,
        6 : six
    }[value](_, x)

#@app.route('/roll')
#def get_roll():
#    print( 'In get_roll()' )
#    start( roll() )
#    return 'ROLL'

@app.route('/start')
def get_start():
    print( 'In get_start()' )
    return 'START'

@app.route('/respond', methods=['GET', 'POST'])
def get_respond():
    print( 'In get_respond()' )
    respond()
    return 'RESPOND'

@app.route('/combine')
def get_combine():
    sense.show_message("Combine")

def send_roll(roll):
    print("Sending roll %d" % (roll,))
    try:
        r = requests.get( 'https://%s.resindevice.io/roll/%d' % (peer_device_uuid, roll))
    except e:
        print(e)

class State:
    TICK_MOD = 5

    def __init__(self):
        self.ticks_mod = 0
        self.cool_down_ticks = 0
        self.prev_dice_value = randint(1, 6)
        self.dice_value = randint(1, 6)
        self.prev_dot_color = blue
        self.dot_color = red
        self.final_dice_value = randint(1, 6)
        self.final_dice_color = [red, blue][self.final_dice_value % 2]
        self.rolling_ticks = 10
        send_roll(self.final_dice_value)

    def tick(self):
        self.ticks_mod = (self.ticks_mod + 1) % State.TICK_MOD
        if self.ticks_mod == 0:
            if self.rolling_ticks > 0:
                self.prev_dice_value = self.dice_value
                prev_dot_color = self.prev_dot_color
                self.prev_dot_color = self.dot_color
                self.dot_color = prev_dot_color
                if self.rolling_ticks > 1:
                    self.dice_value = randint(1, 6)
                elif self.final_dice_color != self.dot_color or self.final_dice_value is None:
                    self.rolling_ticks = self.rolling_ticks + 1
                    self.dice_value = randint(1, 6)
                else:
                    self.dice_value = self.final_dice_value
                    self.final_dice_value = None
                    self.final_dice_color = None
                    self.cool_down_ticks = 10

            self.rolling_ticks = max(self.rolling_ticks - 1, 0)
            self.cool_down_ticks = max(self.cool_down_ticks - 1, 0);

        if self.rolling_ticks > 0:
            sense.set_pixels(merge(int_mod6_to_string(self.prev_dice_value, black, self.prev_dot_color), int_mod6_to_string(self.dice_value, black, self.dot_color), 1 - self.ticks_mod / State.TICK_MOD))
        else:
            sense.set_pixels(int_mod6_to_string(self.dice_value, black, self.dot_color))

    def roll(self, delta):
        if self.cool_down_ticks == 0 and self.rolling_ticks == 0:
            self.final_dice_value = randint(1, 6)
            self.final_dice_color = [red, blue][self.final_dice_value % 2]
            self.rolling_ticks = 10
            send_roll(self.final_dice_value)
        if self.cool_down_ticks > 0:
            self.cool_down_ticks = min(self.cool_down_ticks + 2, 10)

    def do_roll(self, roll):
        if self.rolling_ticks == 0:
            self.final_dice_value = roll
            self.final_dice_color = [red, blue][self.final_dice_value % 2]
            self.rolling_ticks = 10

state = State()

class AccelerometerWatcher:
    def __init__(self):
        sense.set_imu_config(False, True, False) 
        self.old_acc = sense.get_accelerometer_raw()

    def tick(self):
        acc = sense.get_accelerometer_raw()
        acc_delta = {'x': acc['x'] - self.old_acc['x'], 'y': acc['y'] - self.old_acc['y'], 'z': acc['z'] - self.old_acc['z']}
        self.old_acc = acc
        if abs(acc_delta['x']) > 0.2 or abs(acc_delta['y']) > 0.2 or abs(acc_delta['z']) > 0.2:
            state.roll(abs(acc_delta['x']) + abs(acc_delta['y']) + abs(acc_delta['z']))
acc_watcher = AccelerometerWatcher()

@app.route('/roll/1')
def recv_roll1():
    roll = 1
    print("Received roll %d" % (roll,))
    state.do_roll(roll)
    return str(randint(1, 6))

@app.route('/roll/2')
def recv_roll2():
    roll = 2
    print("Received roll %d" % (roll,))
    state.do_roll(roll)
    return str(randint(1, 6))

@app.route('/roll/3')
def recv_roll3():
    roll = 3
    print("Received roll %d" % (roll,))
    state.do_roll(roll)
    return str(randint(1, 6))

@app.route('/roll/4')
def recv_roll4():
    roll = 4
    print("Received roll %d" % (roll,))
    state.do_roll(roll)
    return str(randint(1, 6))

@app.route('/roll/5')
def recv_roll5():
    roll = 5
    print("Received roll %d" % (roll,))
    state.do_roll(roll)
    return str(randint(1, 6))

@app.route('/roll/6')
def recv_roll6():
    roll = 6
    print("Received roll %d" % (roll,))
    state.do_roll(roll)
    return str(randint(1, 6))

def tick():
    acc_watcher.tick()
    state.tick()
    threading.Timer(0.0025, tick, ()).start()

if __name__ == '__main__':
    tick()
    app.run(host='0.0.0.0', port=80)

