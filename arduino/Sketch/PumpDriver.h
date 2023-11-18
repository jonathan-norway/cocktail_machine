#ifndef PumpDriver_h
#define PumpDriver_h
#include <Arduino.h>
class PumpDriver {
public:
  PumpDriver(int i2c_addr, int number_of_pumps, int start_pin);
  void run_until_done();
  void i2c_event_handler(int howMany);
private:
  int _i2c_addr;
  int _number_of_pumps;
  int _start_pin;
  long _timeouts[];
  void _assign_output_pins_for_pumps();
  void _stop_pump_if_timeout_reached();
  void _start_pump(int pump_number);
  void _stop_pump(int pump_number);
  void _start_timer(int pump_number, int milliseconds);
  void _setup();
};
#endif