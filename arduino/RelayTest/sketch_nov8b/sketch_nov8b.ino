
#define START_PIN 8
#define PIN_COUNT 2

void setup() {
  // put your setup code here, to run once:
    pinMode(8, OUTPUT);
}
int current_pin = 0;
void loop() {
  // put your main code here, to run repeatedly:
  
  digitalWrite(8, HIGH);
  delay(2000);
  digitalWrite(8, LOW);
  delay(2000);
}
