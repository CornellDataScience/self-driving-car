#include <Arduino.h>
#include <Servo.h>

int incoming = 0;

Servo myservo;

void execute()
{
    if (Serial.available() > 0)
    {
        delay(10);
        int x = Serial.readStringUntil('\n').toInt();
        Serial.println(x * 100);
    }
}

void setup()
{
    Serial.begin(115200);
}

void loop()
{
    // put your main code here, to run repeatedly:
    execute();
}