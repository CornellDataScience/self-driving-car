#include "MotorControlTask.hpp"

MotorControlTask::MotorControlTask(StateFieldRegistry &registry, 
    unsigned int offset)
    : TimedControlTask<void>(registry, "downlink_control_task", offset)
    {
        thrust_commands_fp = find_internal_field<lin::Vector2f>("gnc_a.thrust_cmds", __FILE__, __LINE__);
        engine_on_fp = find_internal_field<bool>("ls.engine_on", __FILE__, __LINE__);

        #ifndef STATIC
        motor1.attach(SERVO::motor1_pin);
        motor2.attach(SERVO::motor2_pin);
        #endif
    }

void MotorControlTask::execute(){
    if(engine_on_fp->get()){
        actuate();
    }
    else{
        motor1.write(0);
        motor2.write(0);
        //If motors is not being actuated, turn both off
    }
}

void MotorControlTask::actuate(){
    lin::Vector2f thrust_commands = thrust_commands_fp->get();
    
    
    DebugSERIAL.print("Motor Output");
    DebugSERIAL.print("(");
    DebugSERIAL.print(thrust_commands(0));
    DebugSERIAL.print(",");
    DebugSERIAL.print(thrust_commands(1)+25);
    DebugSERIAL.println(")");
    
    
    

    motor1.write(thrust_commands(0));
    motor2.write(thrust_commands(1)+25);
}