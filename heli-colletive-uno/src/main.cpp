#include <Arduino.h>
#include <AccelStepper.h>

#define PIN_STEPPER_DIR 7
#define PIN_STEPPER_PULSE 4
#define PIN_STEPPER_EN 8

#define AXIS_Z = 1;

AccelStepper stepper = AccelStepper(1, PIN_STEPPER_PULSE, PIN_STEPPER_DIR);

uint8_t readingCommand = 0;
uint8_t commandAxis = 0;
uint8_t commandIndex = 0;
char command[10];
int zPos = 0;

// enable Z: <1ON>
// disable Z: <1OFF>
// move around clokwise Z: <1+360>
// move around anticlokwise Z: <1-360>

void setup() {
  Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
  pinMode(LED_BUILTIN, OUTPUT);
  stepper.setEnablePin(PIN_STEPPER_EN);
  stepper.setPinsInverted(false, false, true);
  stepper.setMaxSpeed(1000);
  stepper.setAcceleration(500);
  stepper.setCurrentPosition(zPos);
}

void proccessCommand() {
  if (strcmp(command,"ON") == 0) {
    stepper.enableOutputs();
  } else if (strcmp(command,"OFF") == 0) {
    stepper.disableOutputs();
  } else if (command[0] == '+' || command[0] == '-') {
    int diff = atoi(command);
    zPos += diff;
    stepper.moveTo(zPos);
    stepper.runToPosition();
  }
}

void loop() {
  while (Serial.available() > 0) {
    char inChar = Serial.read();
    if (!readingCommand && inChar == '<') {
      readingCommand = 1;
      commandAxis = 0;
      commandIndex = 0;
    } else if (inChar == '>') {
      readingCommand = 0;
      command[commandIndex] = 0;
      proccessCommand();
    } else if (readingCommand && !commandAxis) {
      commandAxis = inChar - '0';
    } else if (readingCommand && commandAxis) {
      command[commandIndex++] = inChar;
    }
  }
  digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
  //stepper.moveTo(800);
  //stepper.runToPosition();
  delay(100);                      // wait for a second
  digitalWrite(LED_BUILTIN, LOW);   // turn the LED off by making the voltage LOW
  //stepper.moveTo(0);
  //stepper.runToPosition();
  delay(1000);         
}