#import motor
from app import app

@app.route('/')
@app.route('/index')
def index():
	return "hello!"

@app.route('/car/start', methods=['POST'])

def init_driver():
    car = MotorDriver(0,50)
    return "Car has started (pwm=50Hz)", 201

@app.route('/car/move', methods=['POST'])

def move_car():
    car.set_direction(request.json['direction'])
    car.set_speed(request.json['speed'])
    turn = request.json.get('turn', False)
    if turn:
        car.turn(turn.json('side'), turn.json('turn_value'))
    return 201


@app.route('/car/stop', methods=['POST'])
def stop_car():
    car.stop()
    return "car shutdown!", 201

@app.route('/car', methods=['GET'])
def car_status():
    return "ok", 200
