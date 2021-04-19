#ifndef LIGHTCONTROLER_H
# define LIGHTCONTROLER_H

# include <Arduino.h>
# include <CapacitiveSensor.h>

# define CAPACITIVE_TRESHHOLD 5000
# define RED_PIN 6
# define GREEN_PIN 9
# define BLUE_PIN 5

class LightController
{
private:
	bool sitting;
	CapacitiveSensor sittingSensor;
public:
	LightController(int capacitiveSendPin, int capacitiveReceivePin);
	LightController() = default;
	bool IsSitting();
	void Update();
	void Setup();
	void ChangeColor(int r, int g, int b);
	void ChangeColor(long color);
};

#endif