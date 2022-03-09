#ifndef SERVO_CONTROL_TASK_HPP_
#define SERVO_CONTROL_TASK_HPP_
#pragma once
#include <Servo.h>

#include "TimedControlTask.hpp"

/**
* @brief Gets inputs from the ADCS box and dumps them into the state
* fields listed below.
*/
class ServoControlTask : public TimedControlTask<void>
{
public:
    /**
     * @brief Construct a new ADCSBoxMonitor control task
     * 
     * @param registry input StateField registry
     * @param offset control task offset
     */
    ServoControlTask(StateFieldRegistry &registry, unsigned int offset);

    /**
    * @brief Gets inputs from the ADCS box and dumps them into the state
    * fields listed below.
    */
    void execute() override;

protected:
    /**
    * @brief Inputs to get from GNC.
    */
    InternalStateField<lin::Vector4f>* flap_commands_fp;
    InternalStateField<bool>* servo_on_fp;
    InternalStateField<lin::Vector4f>* fin_commands_fp;
    
    Servo flap1;
    Servo flap2;
    Servo flap3;
    Servo flap4;

    Servo fin1;
    Servo fin2;
    Servo fin3;
    Servo fin4;


    void terminate();
    void actuate();
};

#endif
