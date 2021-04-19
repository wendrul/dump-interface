#include <Arduino.h>
#include <CapacitiveSensor.h>
#include "LightController.h"

#define SEND_PIN 4
#define RECEIVE_PIN 2
#define GREEN_COLOR 0x007706
#define RED_COLOR 0x780010

LightController *Lights;

void setup()
{
	Lights = new LightController(SEND_PIN, RECEIVE_PIN);
}

void loop()
{
	Lights->Update();
	if (Lights->IsSitting())
		Lights->ChangeColor(RED_COLOR);
	else
		Lights->ChangeColor(GREEN_COLOR);
}