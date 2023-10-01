#include <Wire.h>
#include "MyClass.h"
// MyClass ledPin(13);
const int arduinoI2CAddress = 0x8;
const int ledPin = 13;
void setup() {
  // put your setup code here, to run once:
  Wire.begin(arduinoI2CAddress);
  Wire.onReceive(receiveEvent);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
}

void receiveEvent(int howMany) {
  while (Wire.available()) {
    char c = Wire.read();
    digitalWrite(ledPin, c);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(100);
}
