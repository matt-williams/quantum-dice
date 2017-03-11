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
