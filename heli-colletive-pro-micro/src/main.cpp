#include <Arduino.h>
#include "ADS1X15.h"
#include <Joystick.h>
#include <AccelStepper.h>
#include <TaskSchedulerDeclarations.h>
#include <TaskScheduler.h>

Scheduler ts;

ADS1115 ADS(0x48);
// Create the Joystick
Joystick_ Joystick(JOYSTICK_DEFAULT_REPORT_ID, 
  JOYSTICK_TYPE_JOYSTICK, 32, 0,
  false, false, false, // X, Y, Z
  false, false, false, // RX, RY, RZ
  false, true, false, // ruder, throtle, accelerator
  false, false // brake, steering
  );


#define ADS_PIN 0
#define ADC_LOW_VALUE 200
#define ADC_HIGH_VALUE 25000

#define PIN_STEPPER_EN 9
#define PIN_STEPPER_DIR 5
#define PIN_STEPPER_PULSE 6
#define PIN_TRIM_RELEASE 7

AccelStepper stepper = AccelStepper(1, PIN_STEPPER_PULSE, PIN_STEPPER_DIR);

void adcCallback() {
  if (ADS.isReady())
  {
    int16_t value = ADS.getValue();
    //Serial.print("Read value ");
    //Serial.println(value);
    Joystick.setThrottle(value);
    ADS.requestADC(ADS_PIN); // request new conversion
  }
}

Task adcTask( 200 * TASK_MILLISECOND, TASK_FOREVER, &adcCallback, &ts, true);


int trimReleaseValue = 1;

void setup()
{
  stepper.setEnablePin(PIN_STEPPER_EN);
  stepper.setMaxSpeed(1000);
  stepper.setAcceleration(500);
  stepper.setPinsInverted(false, false, true);
  pinMode(PIN_TRIM_RELEASE, INPUT_PULLUP);
  // pinMode(PIN_STEPPER_PULSE, OUTPUT);
  // digitalWrite(PIN_STEPPER_DIR, 0);
  Serial.begin(115200);
  ADS.begin();
  if (ADS.isConnected())
  {
    Serial.println("ADS connected");
    ADS.setGain(0); // 6.144 volt
    ADS.setMode(1); // SINGLE SHOT MODE
    ADS.requestADC(ADS_PIN);
  }
  else
  {
    Serial.println("ADS not connected");
  }
  Joystick.setThrottleRange(ADC_LOW_VALUE, ADC_HIGH_VALUE);
  Joystick.begin(); // auto send
}

void loop()
{
  ts.execute();
  stepper.run();
  int currentTr = digitalRead(PIN_TRIM_RELEASE);
  if (currentTr != trimReleaseValue) {
    trimReleaseValue = currentTr;
    if (currentTr) {
      stepper.enableOutputs();
      Serial.println("Trim lock activated");
    } else {
      stepper.disableOutputs();
      Serial.println("Trim lock released");
    }
  }
}