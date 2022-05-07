#include <Arduino.h>
#include <Math.h>

#define DIR_PIN_1 2
#define STEP_PIN_1 3
#define DIR_PIN_2 4
#define STEP_PIN_2 5

const int drive_to_stepper = 9;
const int max_step_size = 100;

int current = 0; // the current stepper motor angle

int target = 0;

// drive_to_stepper_angle(drive) is the discrete stepper motor value that corresponds to a drive angle on the steering wheel
int drive_to_stepper_angle(int drive)
{
    return drive * drive_to_stepper;
}

void turn_motor(int num_steps)
{
    if (num_steps > 0)
    {
        digitalWrite(DIR_PIN_1, HIGH);
        digitalWrite(DIR_PIN_2, HIGH);
    }
    else
    {
        digitalWrite(DIR_PIN_1, LOW);
        digitalWrite(DIR_PIN_2, LOW);
    }
    for (int i = 0; i < abs(num_steps); i++)
    {
        digitalWrite(STEP_PIN_1, HIGH);
        digitalWrite(STEP_PIN_2, HIGH);
        delayMicroseconds(100);
        digitalWrite(STEP_PIN_1, LOW);
        digitalWrite(STEP_PIN_2, LOW);
        delayMicroseconds(100);
    }
    current += num_steps;
}

void execute()
{
    if (Serial.available() > 0)
    {
        delay(10);
        target = Serial.readString().toInt(); // the target driving wheel angle
    }

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

void setup()
{
    Serial.setTimeout(10);
    pinMode(STEP_PIN_1, OUTPUT);
    pinMode(STEP_PIN_2, OUTPUT);
    pinMode(DIR_PIN_1, OUTPUT);
    pinMode(DIR_PIN_2, OUTPUT);
    digitalWrite(STEP_PIN_1, LOW);
    digitalWrite(STEP_PIN_2, LOW);
    Serial.begin(115200);
}

void loop()
{
    // put your main code here, to run repeatedly:
    execute();
    // turn_motor(-1000);
}