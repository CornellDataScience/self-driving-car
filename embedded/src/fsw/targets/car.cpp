#include <Arduino.h>
#include <Servo.h>
#include <Math.h>

const int drive_to_stepper = 5;
const int step_size = 10;

int current = 0; //the current stepper motor angle

//drive_to_stepper_angle(drive) is the discrete stepper motor value that corresponds to a drive angle on the steering wheel
int drive_to_stepper_angle(int drive) {
    return drive * drive_to_stepper;
}

void turn_motor(int num_steps) {
    if(num_steps > 0) {
        for(int i = 0; i < num_steps; i++) {
            //turn motor one degree right
        }
    }
    else {
        for(int i = 0; i < abs(num_steps); i++) {
            //turn motor one degree left
        }
    }
}

void execute()
{
    if (Serial.available() > 0)
    {
        delay(10);
        int target = Serial.readStringUntil('\n').toInt(); //the target driving wheel angle
        int differential = drive_to_stepper_angle(target) - current;
        if(differential > step_size) {
            turn_motor(step_size);
        }
        else if(differential < step_size && differential > 0) {
            turn_motor(differential);
        }
        else if(differential == 0) {
            turn_motor(0);
        }
        else { //differential < step_size && differential < 0
            if(abs(differential) > step_size) {
                turn_motor(step_size * -1);
            }
            else {
                turn_motor(differential);
            }
        }
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