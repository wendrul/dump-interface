#include <Arduino.h>
#include <CapacitiveSensor.h>


#define RED_PIN 6
#define GREEN_PIN 9
#define BLUE_PIN 5

CapacitiveSensor   cs_4_2 = CapacitiveSensor(4,2);

void changeColor(int r, int g, int b)
{
	analogWrite(RED_PIN, r);
	analogWrite(GREEN_PIN, g);
	analogWrite(BLUE_PIN, b);
}

void changeColor(long color)
{
	int r,g,b;

	r = (color >> 16) & 255;
	g = (color >> 8) & 255;
	b = color & 255;
	changeColor(r, g, b);
}

void setup()
{
	cs_4_2.set_CS_AutocaL_Millis(0xFFFFFFFF);
	pinMode(RED_PIN, OUTPUT);
	pinMode(BLUE_PIN, OUTPUT);
	pinMode(GREEN_PIN, OUTPUT);
}

void loop()
{
	long ret = cs_4_2.capacitiveSensor(30);
	if (ret > 5000)
		changeColor(0x780010);
	else
		changeColor(0x007706);
}