package main
// #cgo LDFLAGS: -lpigpiod_if -lrt -lpthread
// #include "pigpiod_if.h"
import "C"
import (
	"fmt"
	"time"
	"encoding/json"
	"net/http"
)
const (
	frontLeft_pin int = 17
	frontRight_pin int = 22
	rearLeft_pin int = 27
	rearRight_pin int = 23

	leftPWM_pin int = 18
	rightPWM_pin int = 25
)
type Car struct{
	frontLeft_pin, frontRight_pin, rearLeft_pin, rearRight_pin int
	leftPWM_pin, rightPWM_pin int
	direction string
	speed int
	status string
}

func (car *Car) init(){
	car.frontLeft_pin = frontLeft_pin
	car.frontRight_pin = frontRight_pin
	car.rearLeft_pin = rearLeft_pin
	car.rearRight_pin = rearRight_pin
	car.leftPWM_pin = leftPWM_pin
	car.rightPWM_pin = rightPWM_pin
	car.status = "Initialiazed"
}

func (car *Car) start(){
	connectPiGPIO()
	initPiGPIO(car.frontLeft_pin,1)
	initPiGPIO(car.frontRight_pin,1)
	initPiGPIO(car.rearLeft_pin,1)
	initPiGPIO(car.rearRight_pin,1)
	initPiPWM(car.leftPWM_pin,50)
	initPiPWM(car.rightPWM_pin,50)
	setPiPWNDutyCyle(car.leftPWM_pin,0)
	setPiPWNDutyCyle(car.rightPWM_pin,0)
	car.status = "Started"
}

func (car *Car) ServeHTTP(w http.ResponseWriter, r *http.Request){
	w.Header().Set("Content-type", "text/plain")
  	if len(car.status) > 0 {
  		var msg string = `{"status":"` + car.status + `"}`
  	}else{
  		http.NotFound(w, r)
  		var msg string = `{"status":"NotExists"}`
  	}
  	jsonMsg, err := json.Marshal(msg)
	if err != nil {
	panic(err)
	}
  fmt.Fprintf(w, string(jsonMsg))

}

func (car *Car) shutdown(){
	writePiGPIO(car.frontLeft_pin, false)
	writePiGPIO(car.frontRight_pin,false)
	writePiGPIO(car.rearLeft_pin,false)
	writePiGPIO(car.rearRight_pin,false)
	writePiGPIO(car.leftPWM_pin,false)
	writePiGPIO(car.rightPWM_pin,false)
	disconnectPiGPIO()
	car.status = "Off"
}

func (car *Car) setDirection(direction string){
	switch direction{
		case "forward":
			writePiGPIO(car.frontLeft_pin, true)
			writePiGPIO(car.rearLeft_pin, false)
			writePiGPIO(car.frontRight_pin, true)
			writePiGPIO(car.rearRight_pin, false)
			car.direction = direction

		case "backward":
			writePiGPIO(car.frontLeft_pin, false)
			writePiGPIO(car.rearLeft_pin, true)
			writePiGPIO(car.frontRight_pin, false)
			writePiGPIO(car.rearRight_pin, true)
			car.direction = direction

		case "rotate":
			writePiGPIO(car.frontLeft_pin, false)
			writePiGPIO(car.rearLeft_pin, true)
			writePiGPIO(car.frontRight_pin, true)
			writePiGPIO(car.rightPWM_pin, false)
			car.direction = direction
	}
	car.status = "Moving"
}

func (car *Car) setSpeed(speed int){
	setPiPWNDutyCyle(car.rightPWM_pin, speed)
	setPiPWNDutyCyle(car.rightPWM_pin, speed)
}

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

func writePiGPIO(pin int, value bool){
	var i int
	if value {
		i=1
	}else{
		i=0
	}
	C.gpio_write(C.uint(pin),C.uint(i))
}

func disconnectPiGPIO(){
	C.pigpio_stop()
}

func rootHandler(w http.ResponseWriter, r *http.Request) {  
  w.Header().Set("Content-type", "text/plain")
  var msg string = `{"status":"OK"}`
  jsonMsg, err := json.Marshal(msg)
  if err != nil {
        panic(err)
    }
  fmt.Fprintf(w, string(jsonMsg))
}




func main(){
	car := new(Car)
	mux := http.NewServeMux()
	
	mux.Handle("/status", car)

  	http.ListenAndServe(":8080", mux)
	car.init()
	car.start()
	car.setDirection("forward")
	car.setSpeed(200)
	time.Sleep(3 * time.Second)
	car.setDirection("backward")
	car.setSpeed(100)
	time.Sleep(5 * time.Second)
	car.shutdown()
}
