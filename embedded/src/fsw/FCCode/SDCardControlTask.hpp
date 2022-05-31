#ifndef SD_CARD_CONTROL_TASK_HPP_
#define SD_CARD_CONTROL_TASK_HPP_
#pragma once

#include "TimedControlTask.hpp"

#include <SD.h>
#include <SPI.h>


/**
* @brief Gets inputs from the ADCS box and dumps them into the state
* fields listed below.
*/
class SDCardControlTask : public TimedControlTask<void>
{
public:
    /**
     * @brief Construct a new ADCSBoxMonitor control task
     * 
     * @param registry input StateField registry
     * @param offset control task offset
     */
    SDCardControlTask(StateFieldRegistry &registry, unsigned int offset);

    /**
    * @brief Gets inputs from the ADCS box and dumps them into the state
    * fields listed below.
    */
    void execute() override;

    const int chipSelect = BUILTIN_SDCARD;
    File myFile;

protected:
    /**
    * @brief Inputs to get from GNC.
    */
    InternalStateField<lin::Vector4f>* flap_commands_fp;
    InternalStateField<bool>* servo_on_fp;
    InternalStateField<lin::Vector4f>* fin_commands_fp;
    InternalStateField<lin::Vector3d>* euler_deg_p;
    InternalStateField<lin::Vector3d>* position_dp;
    InternalStateField<lin::Vector3d>* a_com_p;
    InternalStateField<lin::Vector3f>* acc_error_fp;
    InternalStateField<lin::Vector3f>* lin_acc_vec_fp;
    InternalStateField<lin::Vector2f>* thrust_commands_fp;
    InternalStateField<lin::Vector3d>* acc_p;




    void actuate();
};

#endif
