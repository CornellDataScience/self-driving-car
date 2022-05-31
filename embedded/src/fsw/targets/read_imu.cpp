#include <Arduino.h>
  
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

#define BNO055_SAMPLERATE_DELAY_MS 100

Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28);
bool led_on = false;

void displaySensorDetails(void)
{
    sensor_t sensor;
    bno.getSensor(&sensor);
    Serial.println("------------------------------------");
    Serial.print  ("Sensor:       "); Serial.println(sensor.name);
    Serial.print  ("Driver Ver:   "); Serial.println(sensor.version);
    Serial.print  ("Unique ID:    "); Serial.println(sensor.sensor_id);
    Serial.print  ("Max Value:    "); Serial.print(sensor.max_value); Serial.println(" xxx");
    Serial.print  ("Min Value:    "); Serial.print(sensor.min_value); Serial.println(" xxx");
    Serial.print  ("Resolution:   "); Serial.print(sensor.resolution); Serial.println(" xxx");
    Serial.println("------------------------------------");
    Serial.println("");
    delay(500);
}

void execute_led()
{
    digitalWrite(13, led_on);
    led_on = !led_on;
}

void execute_sensor(){
        /* Get a new sensor event */
    sensors_event_t event;
    bno.getEvent(&event);

    /* Board layout:
            +----------+
            |         *| RST   PITCH  ROLL  HEADING
        ADR |*        *| SCL
        INT |*        *| SDA     ^            /->
        PS1 |*        *| GND     |            |
        PS0 |*        *| 3VO     Y    Z-->    \-X
            |         *| VIN
            +----------+
    */

    /* The processing sketch expects data as roll, pitch, heading */
    /*
    Serial.print(F("Orientation: "));
    Serial.print((float)event.magnetic.x);
    Serial.print(F(" "));
    Serial.print((float)event.magnetic.y);
    Serial.print(F(" "));
    Serial.print((float)event.magnetic.z);
    Serial.println(F(""));
    */

    Serial.print(event.magnetic.x);
    

    /* Also send calibration data for each sensor. */
    /*
    uint8_t sys, gyro, accel, mag = 0;
    bno.getCalibration(&sys, &gyro, &accel, &mag);
    Serial.print(F("Calibration: "));
    Serial.print(sys, DEC);
    Serial.print(F(" "));
    Serial.print(gyro, DEC);
    Serial.print(F(" "));
    Serial.print(accel, DEC);
    Serial.print(F(" "));
    Serial.println(mag, DEC);
    */

    delay(BNO055_SAMPLERATE_DELAY_MS);
}

void setup()
{
    // put your setup code here, to run once:
    pinMode(13, OUTPUT);
    Serial.begin(115200);

    if(!bno.begin())
    {
        /* There was a problem detecting the BNO055 ... check your connections */
        Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
        while(1);
    }

    delay(1000);

    /* Use external crystal for better accuracy */
    bno.setExtCrystalUse(true);

    /* Display some basic information on this sensor */
    displaySensorDetails();
}

void loop()
{
    // put your main code here, to run repeatedly:
    execute_led();
    execute_sensor();
    Serial.write("Execute Cycle\n");
}