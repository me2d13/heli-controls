#include <Arduino.h>
#include "ADS1X15.h"
#include <Joystick.h>
#include <TaskSchedulerDeclarations.h>
#include <TaskScheduler.h>
#include <Bounce2.h>

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

Bounce bounce = Bounce(); // Instantiate a Bounce object  


#define ADS_PIN 0
#define ADC_LOW_VALUE 200
#define ADC_HIGH_VALUE 25000

#define PIN_TRIM_RELEASE 4

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


int eventNo = 1;

void setup()
{
  bounce.attach(PIN_TRIM_RELEASE,INPUT_PULLUP); // Attach the debouncer to a pin with INPUT_PULLUP mode
  bounce.interval(25); // Use a debounce interval of 25 milliseconds
  // pinMode(PIN_STEPPER_PULSE, OUTPUT);
  // digitalWrite(PIN_STEPPER_DIR, 0);
  Serial1.begin(9600);
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
  bounce.update(); // Update the Bounce instance
  if (bounce.changed()) {
    Serial.print("Event #");
    Serial.print(eventNo++);
    Serial.print(": ");
    if (bounce.rose()) {
      Serial1.println("<1ON>");
      Serial.println("Trim lock activated");
    } else {
      Serial1.println("<1OFF>");
      Serial.println("Trim lock released");
    }
  }
}