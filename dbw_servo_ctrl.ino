/* Sweep
Arduino script to control Servo motor according to input from serial
*/

#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position
int incomingByte = 0;   // for incoming serial data

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
   Serial.begin(9600);
   myservo.writeMicroseconds(1500);  // set servo to mid-point
}

int angle;
void loop() {
  Serial.println("Hello world from Ardunio!"); // write a string
  delay(1000);
 
  while (Serial.available()==0){}             // wait for user input
  String a = Serial.readString();
  Serial.println("Received Value: ");
  Serial.println(a);
  angle = a.toInt();

  myservo.write(angle); 

}

