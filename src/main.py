from flask import Flask
from sense_hat import SenseHat

app = Flask(__name__)
sense = SenseHat()

@app.route('/')
def hello_world():
    sense.show_message("Hello world!")
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

sense = SenseHat()

X = [255, 0, 0]
O = [255, 255, 255]

six = [
X, X, O, X, X, O, X, X,
X, X, O, X, X, O, X, X,
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O,
X, X, O, O, O, O, O, O,
X, X, O, O, O, O, O, O,
]

sense.set_pixels(six)
