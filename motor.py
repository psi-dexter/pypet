import RPi.GPIO as io
io.setmode(io.BCM)

class MotorDriver(object):
    """
    Class controlled L293D driver controller
    """
    def __init__(self, speed, pwm_freq=50):
        self.pwm_freq = pwm_freq #pwm frequency
        self.in_fl = 17 #front left motor in_pin_1
        self.in_rl = 27  #rear left motor in_pin_2

        self.in_fr = 22 #front right motor in_pin_3
        self.in_rr = 23 #rear right motor in_pin_4

        self.pwm_left_pin = 18 #leftside  speed control
        self.pwm_right_pin = 25 #rightside  speed control

        self.pwm_left = io.PWM(pwm_left_pin, self.pwm_freq)
        self.pwm_right = io.PWM(pwm_right_pin, self.pwm_freq)

        io.setup(self.in_fl, io.OUT)
        io.setup(self.in_rl, io.OUT)
        io.setup(self.in_fr, io.OUT)
        io.setup(self.in_rr, io.OUT)
        io.setup(self.pwm_left, io.OUT)
        io.setup(self.pwm_right, io.OUT)

        self.set_direction("forward")

        self.set_speed(0)

    def set_direction(direction):
        if direction == "forward":
            io.output(in1_pin, True)
            io.output(in2_pin, False)
            io.output(in3_pin, True)
            io.output(in4_pin, False)

        elif direction == "backward":
            io.output(in1_pin, False)
            io.output(in2_pin, True)
            io.output(in3_pin, False)
            io.output(in4_pin, True)

        elif direction == "rotate":
            io.output(in1_pin, False)
            io.output(in2_pin, True)
            io.output(in3_pin, True)
            io.output(in4_pin, False)
        self.current_direction = direction
        return direction

    def turn_to_left(value):
        self.pwm_left.ChangeDutyCycle(self.current_speed*value)

    def turn_to_right(value):
        self.pwm_right.ChangeDutyCycle(self.current_speed*value)

    def set_speed(speed):
        self.pwm_left.ChangeDutyCycle(speed)
        self.pwm_right.ChangeDutyCycle(speed)
        self.current_speed = speed
        return speed

    def stop():
        self.pwm_left.stop()
        self.pwm_right.stop()
        io.cleanup()


while True:
    motor = MotorDriver(0,50)
    direction_map = {"f":"forward",
                     "b":"backward",
                     "c":"rotate",
                     "l":"turn_to_left",
                     "r":"turn_to_right"   }
    cmd = raw_input("Command, f/b/l/r/x(for exit) 0..100, E.g. f5 :")
    speed = (float(cmd[1:]))
    if direction_map[cmd[0]]:
        motor.set_direction(direction_map[cmd[0]])
        motor.set_speed(speed)
    elif cmd[0] == "x":
        motor.stop()
        break
    else
        printf("command not found")
