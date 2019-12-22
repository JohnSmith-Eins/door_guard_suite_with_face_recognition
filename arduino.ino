#include <Servo.h>

Servo myservo;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  myservo.attach(9);
}

void loop() {
  // put your main code here, to run repeatedly:
  int n= analogRead(A3);
  Serial.println(n);
  if(n>300)
    myservo.write(90);
  else myservo.write(30);
  delay(100); 
}
