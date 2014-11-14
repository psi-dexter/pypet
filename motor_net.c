#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "pigpiod_if.h"

#define nfrontLeft_pin 17;
#define nfrontRight_pin 22;
#define nrearLeft_pin 27;
#define nrearRight_pin 23;
#define nleftPWM_pin 18;
#define nrightPWM_pin 25;

typedef struct {
	int frontLeft_pin,frontRight_pin,rearLeft_pin,rearRight_pin;
	int leftPWM_pin,rightPWM_pin;
} MOTOR;

MOTOR *newCar (int frontLeft_pin, int frontRight_pin, int rearLeft_pin, int rearRight_pin, int leftPWM_pin, int rightPWM_pin)
{
	MOTOR *car;
	car=(MOTOR*)malloc(sizeof(MOTOR));
	car->frontLeft_pin = frontLeft_pin;
	car->frontRight_pin = frontRight_pin;
	car->rearLeft_pin = rearLeft_pin;
	car->rearRight_pin = rearRight_pin;
	car->leftPWM_pin = leftPWM_pin;
	car->rightPWM_pin = rightPWM_pin;
}

int initMotorDriver(MOTOR *car)
{
	pigpio_start(NULL,NULL);
	set_mode(car->frontLeft_pin, 1);
	set_mode(car->frontRight_pin, 1);
	set_mode(car->rearLeft_pin, 1);
	set_mode(car->rearRight_pin, 1);
	set_mode(car->leftPWM_pin, 1);
	set_mode(car->rightPWM_pin, 1);
	set_PWM_frequency(car->leftPWM_pin, 50);
	set_PWM_frequency(car->rightPWM_pin, 50);
}

int stopMotorDriver()
{
	pigpio_stop();
}
void moveForward(MOTOR *car, int speed)
{
	set_PWM_dutycycle(car->leftPWM_pin, speed);
	set_PWM_dutycycle(car->rightPWM_pin, speed);
}


int main(void)
{
	MOTOR *simpleCar;
	simpleCar = newCar(17, 22, 27, 23, 18, 25);
	int speed, rotate_multiply;
	char direction[1];
	initMotorDriver(simpleCar);
	while(1)
	{
		printf("Command, f/b/l/r/x(for exit) 0..255, E.g. f90 :");
		scanf("%s%d", &direction, &speed);
		if(*direction == 'f')
		{
			moveForward(simpleCar,speed);
		}
		if(*direction == 'x')
		{
			stopMotorDriver();
			return 0;
		}

		printf("Direction: %s, Speed: %d /n", direction, speed);
	}
	return 0;
}
