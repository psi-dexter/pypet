from motor import MotorDriver
from flask import jsonify, abort, request
from app import app
car = MotorDriver(50)
@app.route('/')
@app.route('/index')
def index():
    return "hello!"

@app.route('/car/start', methods=['POST'])

def init_driver():
    car.start()
    return "Car has started (pwm=50Hz)", 201

@app.route('/car/move', methods=['POST'])

def move_car():
    car.set_direction(str(request.json['direction']))
    car.set_speed(float(request.json['speed']))
    turn = request.json.get('turn', False)
    if turn:
        car.turn(str(turn.json('side')), float(turn.json('turn_value')))
    return 201

@app.route('/car/stop', methods=['POST'])
def stop_car():
    car.stop()
    return "car shutdown!", 201

@app.route('/car', methods=['GET'])
def car_status():
    return "ok", 200
