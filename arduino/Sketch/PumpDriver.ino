#include "Arduino.h"
#include "PumpDriver.h"
#include "Wire.h"

const int NUMBER_OF_PUMPS = 5;
const int STARTING_PIN = 8;
const int ARDUINO_ADDRESS_1 = 0x4;
const int ARDUINO_ADDRESS_2 = 0x5;

const int CURRENT_ARDUINO_ADDRESS = ARDUINO_ADDRESS_1;

PumpDriver pump_driver(CURRENT_ARDUINO_ADDRESS, NUMBER_OF_PUMPS, STARTING_PIN);


void setup() {
  // put your setup code here, to run once:
  Wire.begin(ARDUINO_ADDRESS_1);
  Wire.onReceive(b);
}

void loop() {
  // put your main code here, to run repeatedly:
  pump_driver.run_until_done();
}

void receiveEvent(int howMany) {
  pump_driver.i2c_event_handler(howMany);
}