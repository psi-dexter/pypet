package main
// #cgo LDFLAGS: -lpigpiod_if -lrt -lpthread
// #include "pigpiod_if.h"
import "C"
import (
	"fmt"
	"time"
	//"encoding/json"
	//"net/http"
	//"strings"
)
const (
	SH_clock_pin int = 17
	DS_serial_pin int = 18
	ST_clock_pin int = 27 // set clock
)

func initRegister() {
	connectPiGPIO()
	initPiGPIO(SH_clock_pin,1)
	initPiGPIO(DS_serial_pin,1)
	initPiGPIO(ST_clock_pin,1)
}

func initPiGPIO(pin, mode int){
	C.set_mode(C.uint(pin), C.uint(mode))
}

func deinitRegister() {
	writePiGPIO(SH_clock_pin,false)
	writePiGPIO(DS_serial_pin,false)
	writePiGPIO(ST_clock_pin,false)
	disconnectPiGPIO()
}


func connectPiGPIO(){
	C.pigpio_start(nil,nil)
}

func disconnectPiGPIO(){
	C.pigpio_stop()
}

func toBool(i int) bool{
	var result bool
	if i == 1 {
		result = true
	} else {
		result = false
	}
	return result
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

func main(){
	fmt.Println("Started...")
	initRegister()
	var afinity string
	afinity = "11100000"
	writePiGPIO(ST_clock_pin,false)
	for i:=0; i<len(afinity);i++{
		writePiGPIO(DS_serial_pin, toBool(int(afinity[i])-48))
		writePiGPIO(SH_clock_pin, true)
		writePiGPIO(SH_clock_pin, false)
		time.Sleep(100 * time.Millisecond)
	}
	writePiGPIO(ST_clock_pin,true)
	time.Sleep(100 * time.Millisecond)
	writePiGPIO(ST_clock_pin,false)
	time.Sleep(100 * time.Millisecond)
	fmt.Println("Stoped...")
	deinitRegister()
}
