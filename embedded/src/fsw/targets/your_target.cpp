#include <Arduino.h>

void execute()
{
    digitalWrite(13, HIGH);
    delay(500);
    digitalWrite(13, LOW);
    delay(500);
    Serial.write("LED cycle\n");
}

void setup()
{
    // put your setup code here, to run once:
    delay(2000);
    pinMode(13, OUTPUT);
    Serial.begin(9600);
}

void loop()
{
    // put your main code here, to run repeatedly:
    execute();
}