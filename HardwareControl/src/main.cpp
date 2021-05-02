#include <Arduino.h>
#include <CapacitiveSensor.h>
#include "LightController.h"

#define SEND_PIN 4
#define RECEIVE_PIN 2
#define GREEN_COLOR 0x007706
#define RED_COLOR 0x780010
#define COMMUNICATION_RATE 100.

LightController *Lights;
unsigned long t;
unsigned long timer;

void setup()
{
	Serial.begin(115200);
	t = millis();
	timer = 0;
	Lights = new LightController(SEND_PIN, RECEIVE_PIN);
}

void loop()
{
	long dt = millis() - t;
	t = millis();
	Lights->Update();
	if (Lights->IsSitting())
		Lights->ChangeColor(RED_COLOR);
	else
		Lights->ChangeColor(GREEN_COLOR);
	timer += dt;
	if (timer >= COMMUNICATION_RATE)
	{
		Serial.print("sitting ");
		if (Lights->IsSitting())
			Serial.print("true");
		else
			Serial.print("false");
		Serial.print(", paperWeight ");
		Serial.println(-1); //For now there is no weight sensor implemented
		timer = 0;
	}
}