import RPi.GPIO as io
io.setmode(io.BCM)

in1_pin = 17 #left motor
in2_pin = 27  #left motor

in3_pin = 22 #right motor
in4_pin = 23 #right motor

pwm_pin = 18 #common speed control

io.setup(in1_pin, io.OUT)
io.setup(in2_pin, io.OUT)
io.setup(in3_pin, io.OUT)
io.setup(in4_pin, io.OUT)
io.setup(pwm_pin, io.OUT)

pwm = io.PWM(pwm_pin, 50)


def forward():
    io.output(in1_pin, True)
    io.output(in2_pin, False)
    io.output(in3_pin, True)
    io.output(in4_pin, False)

def backward():
    io.output(in1_pin, False)
    io.output(in2_pin, True)
    io.output(in3_pin, False)
    io.output(in4_pin, True)

def rotate():
    io.output(in1_pin, False)
    io.output(in2_pin, True)
    io.output(in3_pin, True)
    io.output(in4_pin, False)


forward()
pwm.start(0)
while True:
    cmd = raw_input("Command, f/r 0..9, E.g. f5 :")
    direction = cmd[0]
    if direction == "f":
        forward()
    elif direction == "r":
        backward()
    elif direction == "x":
        pwm.stop()
        io.cleanup()
        break
    else:
        rotate()
    pwm.ChangeDutyCycle(int(cmd[1:]))

