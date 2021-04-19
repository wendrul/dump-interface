#include "LightController.h"

LightController::LightController(int capacitiveSendPin, int capacitiveReceivePin):
	sittingSensor{CapacitiveSensor(capacitiveSendPin, capacitiveReceivePin)}
{
	this->sitting = false;
	this->sittingSensor.set_CS_AutocaL_Millis(0xFFFFFFFF);
	pinMode(RED_PIN, OUTPUT);
	pinMode(BLUE_PIN, OUTPUT);
	pinMode(GREEN_PIN, OUTPUT);
}

bool LightController::IsSitting()
{
	return this->sitting;
}

void LightController::Update()
{
	long ret = this->sittingSensor.capacitiveSensor(30);
	if (ret > CAPACITIVE_TRESHHOLD)
		this->sitting = true;
	else
		this->sitting = false;
}

void LightController::ChangeColor(long color)
{
	int r,g,b;

	r = (color >> 16) & 255;
	g = (color >> 8) & 255;
	b = color & 255;
	ChangeColor(r, g, b);
}

void LightController::ChangeColor(int r, int g, int b)
{
	analogWrite(RED_PIN, r);
	analogWrite(GREEN_PIN, g);
	analogWrite(BLUE_PIN, b);
}