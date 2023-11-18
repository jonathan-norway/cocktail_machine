#include "Arduino.h"
#include "PumpDriver.h"
#include "Wire.h"

PumpDriver::PumpDriver(int i2c_addr, int number_of_pumps, int start_pin) {
  _number_of_pumps = number_of_pumps;
  _i2c_addr = i2c_addr;
  _start_pin = start_pin;

  PumpDriver::_assign_output_pins_for_pumps();
  long _timeouts[number_of_pumps]{};
  Serial.begin(9600);
}

void PumpDriver::_assign_output_pins_for_pumps() {
  for (int i = 0; i < _number_of_pumps; i++) {
    pinMode(i + _start_pin, OUTPUT);
    _stop_pump(i);
  }
}


void PumpDriver::i2c_event_handler(int howMany) {
  // Why do we need to empty the buffer?
  if (howMany != 5) {
    Serial.print("Garbage - expected 5 bytes but received: ");
    Serial.println(howMany);
    while (Wire.available()) {
      Wire.read();
    }
    return;
  }

  int garbage_byte_1 = Wire.read();
  int garbage_byte_2 = Wire.read();
  Serial.print("First garbage byte: ");
  Serial.println(garbage_byte_1);
  Serial.print("Second garbage byte: ");
  Serial.println(garbage_byte_2);

  int pump_number = Wire.read();
  int most_significant_time_bit = Wire.read() << 8;
  int least_significant_time_bit = Wire.read();
  int milliseconds = most_significant_time_bit + least_significant_time_bit;

  Serial.print("Pump number ");
  Serial.print(pump_number);
  Serial.print(": ");
  Serial.print(milliseconds);
  Serial.println("ms");

  _start_pump(pump_number);
  _start_timer(pump_number, milliseconds);
}

void PumpDriver::_start_timer(int pump_number, int milliseconds) {
  const long now = millis();
  _timeouts[pump_number] = now + milliseconds;
}

void PumpDriver::_start_pump(int pump_number) {
  // Pumps are connected from PIN 8 and up
  digitalWrite(pump_number + _start_pin, LOW); // Shouldnt it be the opposite?
  Serial.print("Starting pump ");
  Serial.println(pump_number);

}

void PumpDriver::_stop_pump(int pump_number) {
    // Pumps are connected from PIN 8 and up
  digitalWrite(pump_number + _start_pin, HIGH); // Shouldnt it be the opposite?
  Serial.print("Stopping pump ");
  Serial.println(pump_number);
}

void PumpDriver::_stop_pump_if_timeout_reached() {
  const long now = millis();
  for (int i = 0; i < _number_of_pumps; i++) {
    if (_timeouts[i] && _timeouts < now) {
      _stop_pump(i);
      _timeouts[i] = 0;
    }
  }
}

void PumpDriver::run_until_done() {
  delay(10);
  _stop_pump_if_timeout_reached();
}