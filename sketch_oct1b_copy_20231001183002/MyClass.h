#ifndef MyClass_h
#define MyClass_h
#include <Arduino.h>
class MyClass {
public:
  MyClass(int pin);
  void myFunction(int blinkRate);
  void toggleLight();
private:
  int _pin;
  bool _status;
};
#endif