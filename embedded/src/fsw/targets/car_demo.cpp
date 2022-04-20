#include <Arduino.h>
#include <Servo.h>

int incoming = 0;

Servo myservo;

void execute()
{
    /*digitalWrite(13, HIGH);
    delay(500);
    digitalWrite(13, LOW);
    delay(500);
    Serial.write("LED cycle\n");
    unsigned char a = 5;
    Serial.printf("%u", a);
    myservo.write(10);*/
    Serial.write(1);
    delay(1000);
}

void setup()
{
    // put your setup code here, to run once:
    myservo.attach(12);
    delay(2000);
    pinMode(13, OUTPUT);
    Serial.begin(115200);
}

void loop()
{
    // put your main code here, to run repeatedly:
    execute();
}