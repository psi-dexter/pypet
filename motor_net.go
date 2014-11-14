package main
// #cgo LDFLAGS: -lpigpiod_if -lrt -lpthread
// #include "pigpiod_if.h"
import "C"
import "time"

func connectPiGPIO(){
	C.pigpio_start(nil,nil)
}

func initPiGPIO(pin, mode int){
	C.set_mode(C.uint(pin), C.uint(mode))
}

func initPiPWM(pin, frequency int){
	C.set_mode(C.uint(pin), 1)
	C.set_PWM_frequency(C.uint(pin), C.uint(frequency))
}
func setPiPWNDutyCyle(pin, duty int){
	C.set_PWM_dutycycle(C.uint(pin), C.uint(duty))
}
func disconnectPiGPIO(){
	C.pigpio_stop()
}


func main(){
	var frontLeft_pin int = 17
	var frontRight_pin int = 22
	var rearLeft_pin int = 27
	var rearFront_pin int = 23

	var leftPWM_pin int = 18
	var rightPWM_pin int = 25

	connectPiGPIO()
	initPiGPIO(frontLeft_pin,1)
	initPiGPIO(frontRight_pin,1)
	initPiGPIO(rearLeft_pin,1)
	initPiGPIO(rearFront_pin,1)
	initPiPWM(leftPWM_pin,50)
	initPiPWM(rightPWM_pin,50)

	setPiPWNDutyCyle(leftPWM_pin, 200)
	setPiPWNDutyCyle(rightPWM_pin, 200)
	time.Sleep(3 * time.Second)
	setPiPWNDutyCyle(leftPWM_pin, 100)
	setPiPWNDutyCyle(rightPWM_pin, 100)
	time.Sleep(5 * time.Second)

	setPiPWNDutyCyle(leftPWM_pin, 0)
	setPiPWNDutyCyle(rightPWM_pin, 0)
	disconnectPiGPIO()
}
