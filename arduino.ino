#include <Mouse.h>

//byte bf[2];
void setup() {
  Serial.begin(9600);
  Mouse.begin();
}

byte bytes[4];
void loop() {
  int x,y; /* use arduino int type of size 4 bytes  */
  if (Serial.available() > 0) {
    Serial.readBytes(bytes, 4);
    x = bytes[0] << 24 | bytes[1] << 16 |  bytes[2] << 8 |  bytes[0];
    Serial.readBytes(bytes, 4);
    y = bytes[0] << 24 | bytes[1] << 16 |  bytes[2] << 8 |  bytes[0];
    Mouse.move(x, y, 0);
    Serial.read();
  }
}