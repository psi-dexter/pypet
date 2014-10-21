import RPi.GPIO as io
io.setmode(io.BCM)

in1_pin = 17 #left motor
in2_pin = 27  #left motor

in3_pin = 22 #right motor
in4_pin = 23 #right motor

pwm_left_pin = 18 #leftside  speed control
pwm_right_pin = 25 #leftside  speed control

io.setup(in1_pin, io.OUT)
io.setup(in2_pin, io.OUT)
io.setup(in3_pin, io.OUT)
io.setup(in4_pin, io.OUT)
io.setup(pwm_left_pin, io.OUT)
io.setup(pwm_right_pin, io.OUT)

pwm_left = io.PWM(pwm_left_pin, 50)
pwm_right = io.PWM(pwm_right_pin, 50)


def forward(speed):
    io.output(in1_pin, True)
    io.output(in2_pin, False)
    io.output(in3_pin, True)
    io.output(in4_pin, False)
    pwm_left.ChangeDutyCycle(speed)
    pwm_right.ChangeDutyCycle(speed)

def backward(speed):
    io.output(in1_pin, False)
    io.output(in2_pin, True)
    io.output(in3_pin, False)
    io.output(in4_pin, True)
    pwm_left.ChangeDutyCycle(speed)
    pwm_right.ChangeDutyCycle(speed)

def rotate(speed):
    io.output(in1_pin, False)
    io.output(in2_pin, True)
    io.output(in3_pin, True)
    io.output(in4_pin, False)
    pwm_left.ChangeDutyCycle(speed)
    pwm_right.ChangeDutyCycle(speed)

def turn_to_left(speed):
    forward()
    pwm_left.ChangeDutyCycle(speed*0.3)
    pwm_right.ChangeDutyCycle(speed)

def turn_to_right(speed):
    forward()
    pwm_left.ChangeDutyCycle(speed)
    pwm_right.ChangeDutyCycle(speed*0.3)




forward()
pwm_left.start(0)
pwm_right.start(0)

while True:
    cmd = raw_input("Command, f/b/l/r/x(for exit) 0..9, E.g. f5 :")
    direction = cmd[0]
    speed = (float(cmd[1:]))

    if direction == "f":
        forward(speed)
    elif direction == "b":
        backward(speed)
    elif direction == "l":
        turn_to_left(speed)
    elif direction == "r":
        turn_to_right(speed)
    elif direction == "x":
        pwm.stop()
        io.cleanup()
        break
    else:
        rotate(speed)

