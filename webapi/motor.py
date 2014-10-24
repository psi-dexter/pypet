import RPi.GPIO as io
io.setmode(io.BCM)

class MotorDriver(object):
    """
    Class controlled L293D driver controller
    """
    def __init__(self, pwm_freq):
        self.pwm_freq = pwm_freq #pwm frequency
        self.in_fl = 17 #front left motor in_pin_1
        self.in_rl = 27  #rear left motor in_pin_2

        self.in_fr = 22 #front right motor in_pin_3
        self.in_rr = 23 #rear right motor in_pin_4

        self.pwm_left_pin = 18 #leftside  speed control
        self.pwm_right_pin = 25 #rightside  speed control

    def start(self):
        io.setup(self.in_fl, io.OUT)
        io.setup(self.in_rl, io.OUT)
        io.setup(self.in_fr, io.OUT)
        io.setup(self.in_rr, io.OUT)
        io.setup(self.pwm_left_pin, io.OUT)
        io.setup(self.pwm_right_pin, io.OUT)


        self.pwm_left = io.PWM(self.pwm_left_pin, self.pwm_freq)
        self.pwm_right = io.PWM(self.pwm_right_pin, self.pwm_freq)
        self.pwm_left.start(0)
        self.pwm_right.start(0)
        self.current_direction = "forward"
        self.current_speed = 0
        self.set_direction("forward")
        self.set_speed(0)

    def set_direction(self, direction):
        if direction == "forward":
            io.output(self.in_fl, True)
            io.output(self.in_rl, False)
            io.output(self.in_fr, True)
            io.output(self.in_rr, False)

        elif direction == "backward":
            io.output(self.in_fl, False)
            io.output(self.in_rl, True)
            io.output(self.in_fr, False)
            io.output(self.in_rr, True)

        elif direction == "rotate":
            io.output(self.in_fl, False)
            io.output(self.in_rl, True)
            io.output(self.in_fr, True)
            io.output(self.in_rr, False)
        self.current_direction = direction
        return direction

    def set_speed(self, speed):
        self.pwm_left.ChangeDutyCycle(speed)
        self.pwm_right.ChangeDutyCycle(speed)
        self.current_speed = speed
        return speed

    def turn(self, side, value):
        if(side == 'left'):
            self.pwm_left.ChangeDutyCycle(self.current_speed*value)
            #print('currentspeed : '+str(self.current_speed))
            #print('left side speed : '+ str(self.current_speed*value))
        elif(side == 'right'):
            self.pwm_right.ChangeDutyCycle(self.current_speed*value)
            #print('currentspeed : '+str(self.current_speed))
            #print('right side speed : '+ str(self.current_speed*value))

    def stop(self):
        self.pwm_left.stop()
        self.pwm_right.stop()
        io.cleanup()

