#ifndef GNC_HPP_
#define GNC_HPP_
#pragma once

#include "TimedControlTask.hpp"
#include "mission_mode_t.enum"
/**
* @brief Gets inputs from the ADCS box and dumps them into the state
* fields listed below.
*/
class GNC : public TimedControlTask<void>
{
public:
    /**
     * @brief Construct a new ADCSBoxMonitor control task
     * 
     * @param registry input StateField registry
     * @param offset control task offset
     */
    GNC(StateFieldRegistry &registry, unsigned int offset);

    /**
    * @brief Gets inputs from the ADCS box and dumps them into the state
    * fields listed below.
    */
    void execute() override;

protected:

    InternalStateField<unsigned char>* mission_mode_fp;
    InternalStateField<lin::Vector3f>* omega_vec_fp;
    InternalStateField<lin::Vector3f>* euler_vec_fp;
    InternalStateField<lin::Vector4d>* quat_fp;

    /**
    * @brief Outputs of GNC
    */
    InternalStateField<lin::Vector4f> flap_commands_f;

    // eventually not needed, just was for debug
    float inc_dir = 0;

    // not real control laws, just cool
    void dispatch_sweep();
    void omega_response();
    void euler_response();
    //

    void dispatch_detumble();
    void dispatch_bellyflop();
};

#endif
