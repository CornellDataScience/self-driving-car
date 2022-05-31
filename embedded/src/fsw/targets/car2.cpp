#include <Arduino.h>
#include <Math.h>

#define DIR_PIN 2
#define STEP_PIN 3

const int drive_to_stepper = 9;
const int max_step_size = 10000;

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
    for (int i = 0; i < abs(num_steps); i++)
    {
        digitalWrite(STEP_PIN, HIGH);
        delayMicroseconds(100);
        digitalWrite(STEP_PIN, LOW);
        delayMicroseconds(100);
    }
    current += num_steps;
}

void execute()
{
    if (Serial.available() > 0)
    {
        delay(10);
        int target = Serial.readString().toInt(); // the target driving wheel angle
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
    Serial.setTimeout(10);
    pinMode(STEP_PIN, OUTPUT);
    pinMode(DIR_PIN, OUTPUT);
    digitalWrite(STEP_PIN, LOW);
    Serial.begin(115200);
    Serial.print(String(current));
}

void loop()
{
    // put your main code here, to run repeatedly:
    execute();
    // turn_motor(-1000);
}