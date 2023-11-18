#include <Adafruit_NeoPixel.h>
#define LED_PIN 6
#define LED_COUNT 35
Adafruit_NeoPixel ring(LED_COUNT, LED_PIN, NEO_RGBW + NEO_KHZ800);

void setup() {
  // put your setup code here, to run once:
  ring.begin();
  ring.show();
  ring.setBrightness(5);
}

void loop() {
  // put your main code here, to run repeatedly:

  for(int i = 0; i < ring.numPixels(); i++) {
    ring.setPixelColor(i, 0, 0, 125, 10);
    ring.show();
    delay(50);
  }

  for(int i = 0; i < ring.numPixels(); i++) {
    ring.setPixelColor(i, 0, 0, 0, 0);
    ring.show();
    delay(50);
  }
}
