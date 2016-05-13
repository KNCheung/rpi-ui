#include <Wire.h>

char reg[256];

void setup() {
  Wire.begin(0x2B);                // join i2c bus with address #8
  Wire.onRequest(requestEvent);    // register event
  Wire.onReceive(receiveEvent);
}

void loop() {
  delay(100);
  reg[0] = analogRead(A0);
  reg[1] = analogRead(A1);
  reg[2] = digitalRead(7)?0x00:0xff;
}

// function that executes whenever data is requested by master
// this function is registered as an event, see setup()

char outputBuffer, regAddr;
void requestEvent() {
  Wire.write(outputBuffer);
}

void receiveEvent(int cnt) {
  while (Wire.available())
    regAddr = Wire.read();
  outputBuffer = reg[regAddr];
}

