#include "ServoControlTask.hpp"

ServoControlTask::ServoControlTask(StateFieldRegistry &registry, 
    unsigned int offset)
    : TimedControlTask<void>(registry, "servo_control_task", offset)
    {
        flap_commands_fp = find_internal_field<lin::Vector4f>("gnc.flap_cmds", __FILE__, __LINE__);
        servo_on_fp = find_internal_field<bool>("ls.servo_on", __FILE__, __LINE__);

        fin_commands_fp = find_internal_field<lin::Vector4f>("gnc_a.fin_cmds", __FILE__, __LINE__);


        #ifndef STATIC
        //flap1.attach(SERVO::flap1_pin);
        //flap2.attach(SERVO::flap2_pin);
        //flap3.attach(SERVO::flap3_pin);
        //flap4.attach(SERVO::flap4_pin);

        fin1.attach(5);
        fin2.attach(20);
        fin3.attach(4);
        fin4.attach(21);
        #endif
    }

void ServoControlTask::execute(){

    if(servo_on_fp->get())
        actuate();
    else{
        // flap1.write(0);
        // flap2.write(0);
        // flap3.write(0);
        // flap4.write(0);

        // nevermind, don't return to 0, just stop moving all together
    }
}

void ServoControlTask::actuate(){
    lin::Vector4f flap_commands = flap_commands_fp->get();
    lin::Vector4f unit_range;
    lin::Vector4f flap_servo_writes;

    lin::Vector4f fin_commands = fin_commands_fp->get();

    // Serial.printf("GNC Commands: %f,%f,%f,%f\n",flap_commands[0],flap_commands[1],flap_commands[2],flap_commands[3]);

    for(unsigned int i = 0; i < SERVO::num_flaps; i++){
        unit_range(i) = (flap_commands(i) - SERVO::flap_cmd_min)/SERVO::servo_cmd_range;
    }
    for(unsigned int i = 0; i < SERVO::num_flaps; i++){
        flap_servo_writes(i) = (unit_range(i) * SERVO::servo_cmd_range) + SERVO::flap_write_min;
    }

    // for(unsigned int i = 0; i < SERVO::num_flaps; i++){
    //     flap_servo_writes(i) = 45;
    // }

    //flap1.write(flap_servo_writes(0));
    //flap2.write(flap_servo_writes(1));
    //flap3.write(flap_servo_writes(2));
    //flap4.write(flap_servo_writes(3));

    //Add 90 degrees, since fin_commands are given with respect to equilibrium. The equilibrium fin position is 90 degrees
    fin1.write(fin_commands(0)+100);
    fin2.write(fin_commands(1)+80);
    fin3.write(fin_commands(2)+90);
    fin4.write(fin_commands(3)+80);

    
    DebugSERIAL.print("Servo: ");
    DebugSERIAL.print("(");
    DebugSERIAL.print(fin_commands(0));
    DebugSERIAL.print(",");
    DebugSERIAL.print(fin_commands(1));
    DebugSERIAL.print(",");
    DebugSERIAL.print(fin_commands(2));
    DebugSERIAL.print(",");
    DebugSERIAL.print(fin_commands(3));
    DebugSERIAL.print(")     ");
    
    
    



}