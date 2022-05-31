#include <Arduino.h>
#include <Servo.h>
Servo motor1;

void execute()
{   
    motor1.write(180);
    /*
    motor1.write(45);
    Serial.print("45");
    delay(2000); 

    motor1.write(55); 
    Serial.print("55");
    delay(2000);

    motor1.write(65);
    Serial.print("65");
    delay(2000); 

    motor1.write(75); 
    Serial.print("75");
    delay(2000);
    */
}

void setup()
{
    // put your setup code here, to run once:
    delay(2000);
    Serial.begin(9600);
    motor1.attach(2);
}

void loop()
{
    execute();
}