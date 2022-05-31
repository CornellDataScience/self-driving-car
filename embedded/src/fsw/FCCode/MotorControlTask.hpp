#ifndef MOTOR_CONTROL_TASK_HPP_
#define MOTOR_CONTROL_TASK_HPP_
#pragma once
#include <Servo.h>

#include "TimedControlTask.hpp"

/**
* @brief Gets inputs from the ADCS box and dumps them into the state
* fields listed below.
*/
class MotorControlTask : public TimedControlTask<void>
{
public:
    /**
     * @brief Construct a new ADCSBoxMonitor control task
     * 
     * @param registry input StateField registry
     * @param offset control task offset
     */
    MotorControlTask(StateFieldRegistry &registry, unsigned int offset);

    /**
    * @brief Gets inputs from the ADCS box and dumps them into the state
    * fields listed below.
    */
    void execute() override;

protected:
    /**
    * @brief Inputs to get from GNC.
    */
    InternalStateField<lin::Vector2f>* thrust_commands_fp;
    InternalStateField<bool>* engine_on_fp;


    
    Servo motor1;
    Servo motor2;



    void terminate();
    void actuate();
};

#endif
