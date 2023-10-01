#include "Arduino.h"
#include "MyClass.h"

MyClass::MyClass(int pin) {
  pinMode(pin, OUTPUT);
  _pin = pin;
  _status = false;
}

void MyClass::myFunction(int blinkRate){
  toggleLight();
  delay(blinkRate);
  toggleLight();
  delay(blinkRate);
}

void MyClass::toggleLight(){
  if (_status) {
    _status = false;
    digitalWrite(_pin, LOW);
  }
  else {
    _status = true;
    digitalWrite(_pin, HIGH);
  }
}