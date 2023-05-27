#include <Servo.h>

Servo shoulderServo;  // Servo object for shoulder motor
Servo elbowServo;     // Servo object for elbow motor

const int shoulderPin = 9;  // Pin for shoulder servo signal
const int elbowPin = 10;    // Pin for elbow servo signal

void setup() {
  Serial.begin(9600);

  shoulderServo.attach(shoulderPin);
  elbowServo.attach(elbowPin);
}

void loop() {
  if (Serial.available() > 0) {
    // Read the serial input string until newline
    String input = Serial.readStringUntil('\n');
    input.trim();

    // Split the input string into shoulder and elbow angles
    int commaIndex = input.indexOf(',');
    if (commaIndex >= 0) {
      String shoulderAngleStr = input.substring(0, commaIndex);
      String elbowAngleStr = input.substring(commaIndex + 1);
      
      // Convert angle strings to integers
      int shoulderAngle = shoulderAngleStr.toInt();
      int elbowAngle = elbowAngleStr.toInt();

      // Map the angles to servo positions (adjust the min/max values according to your servo)
      int shoulderPosition = map(shoulderAngle, 0, 180, 0, 180);  // Shoulder servo range is 0-180
      int elbowPosition = map(elbowAngle, 0, 180, 0, 180);        // Elbow servo range is 0-180

      // Set the servo positions
      shoulderServo.write(shoulderPosition);
      elbowServo.write(elbowPosition);
    }
  }
}
