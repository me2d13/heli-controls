#include <Arduino.h>
#include "ADS1X15.h"
#include <Joystick.h>
#include <TaskSchedulerDeclarations.h>
#include <TaskScheduler.h>
#include <Bounce2.h>
#include <CD74HC4067.h>

Scheduler ts;

ADS1115 ADS(0x48);
// Create the Joystick
Joystick_ Joystick(JOYSTICK_DEFAULT_REPORT_ID, 
  JOYSTICK_TYPE_JOYSTICK, 32, 0,
  true, true, false, // X, Y, Z
  false, false, false, // RX, RY, RZ
  false, true, false, // ruder, throtle, accelerator
  false, false // brake, steering
  );

Bounce bounce = Bounce(); // Instantiate a Bounce object  

               // s0 s1 s2 s3
CD74HC4067 theMux(18, 19, 20, 21);  // create a new CD74HC4067 object with its four control pins

#define ADS_PIN_MAX 2
#define ADC_LOW_VALUE 200
#define ADC_HIGH_VALUE 25000
#define X_LOW_VALUE 4100
#define X_HIGH_VALUE 12300
#define Y_LOW_VALUE 5500
#define Y_HIGH_VALUE 15000

#define PIN_TRIM_RELEASE 4
#define CYCLIC_PIN_MUX 16
#define MUX_TOTAL_PINS 8

//Task adcTask( 200 * TASK_MILLISECOND, TASK_FOREVER, &adcCallback, &ts, true);


int eventNo = 1;
int adsPin = 0;
int tick = 0;
int currentMuxPin = 0;
int16_t xValue;
int16_t yValue;
int16_t throttleValue;

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
    ADS.requestADC(adsPin);
  }
  else
  {
    Serial.println("ADS not connected");
  }
  Joystick.setThrottleRange(ADC_LOW_VALUE, ADC_HIGH_VALUE);
  Joystick.setXAxisRange(X_LOW_VALUE, X_HIGH_VALUE);
  Joystick.setYAxisRange(Y_LOW_VALUE, Y_HIGH_VALUE);
  Joystick.begin(); // auto send
  pinMode(CYCLIC_PIN_MUX, INPUT_PULLUP);
}

void handleAxis() {
if (ADS.isReady()) {
    int16_t value = ADS.getValue();
    switch (adsPin)
    {
    case 1:
      xValue = X_HIGH_VALUE - value + X_LOW_VALUE;
      Joystick.setXAxis(xValue);
      break;
    case 2:
      Joystick.setYAxis(value);
      yValue = value;
      break;
    default:
      Joystick.setThrottle(value);
      throttleValue = value;
      break;
    }
    if (++adsPin > ADS_PIN_MAX) {
      adsPin = 0;
    }
    ADS.requestADC(adsPin); // request new conversion
    if (++tick > 100) {
      tick = 0;
      Serial.print("Value X: ");
      Serial.print(xValue);
      Serial.print(", Y: ");
      Serial.print(yValue);
      Serial.print(", throttle: ");
      Serial.print(throttleValue);
      Serial.println(".");
    }
  }
}

void handleButtons() {
  theMux.channel(currentMuxPin);
  Joystick.setButton(currentMuxPin, !digitalRead(CYCLIC_PIN_MUX));
  if (++currentMuxPin >= MUX_TOTAL_PINS) {
    currentMuxPin = 0;
  }
}

void loop()
{
  //ts.execute();
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
  handleAxis();
  handleButtons();
}