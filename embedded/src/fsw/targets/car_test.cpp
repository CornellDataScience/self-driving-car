#include <Arduino.h>
#include <Servo.h>
#include <Math.h>

#define DIR_PIN 35
#define STEP_PIN 36

const int drive_to_stepper = 5;
const int max_step_size = 10;

int current = 0; // the current stepper motor angle

// drive_to_stepper_angle(drive) is the discrete stepper motor value that corresponds to a drive angle on the steering wheel
int drive_to_stepper_angle(int drive)
{
    return drive * drive_to_stepper;
}

void turn_motor(int num_steps)
{
    if (num_steps > 0)
        digitalWrite(DIR_PIN, HIGH);
    else
        digitalWrite(DIR_PIN, LOW);
    for (int i = 0; i < num_steps; i++)
    {
        digitalWrite(STEP_PIN, HIGH);
        delayMicroseconds(500);
        digitalWrite(STEP_PIN, LOW);
        delayMicroseconds(500);
    }
    current += num_steps;
}

void execute()
{
    if (true) // Serial.available > 0
    {
        delay(10);
        // int target = Serial.readStringUntil('\n').toInt(); // the target driving wheel angle
        int target = 1000;
        int differential = drive_to_stepper_angle(target) - current;
        int to_step = 0;

        if (differential >= 0)
        {
            to_step = min(differential, max_step_size);
            turn_motor(to_step);
        }
        else
        {
            to_step = max(differential, -1 * max_step_size);
            turn_motor(to_step);
        }
    }
}

void setup()
{
    pinMode(STEP_PIN, OUTPUT);
    pinMode(DIR_PIN, OUTPUT);
    digitalWrite(STEP_PIN, LOW);
    Serial.begin(115200);
}

void loop()
{
    // put your main code here, to run repeatedly:
    execute();
}