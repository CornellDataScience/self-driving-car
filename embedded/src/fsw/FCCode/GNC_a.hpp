#ifndef GNC_a_HPP_
#define GNC_a_HPP_
#pragma once

#include <math.h>
#include "TimedControlTask.hpp"
#include "mission_mode_t.enum"
#include "GPSMonitor.hpp"
#include "adcs_mode_t.enum"


/**
* @brief Gets inputs from the ADCS box and dumps them into the state
* fields listed below.
*/
class GNC_a : public TimedControlTask<void>
{
public:
    /**
     * @brief Construct a new ADCSBoxMonitor control task
     * 
     * @param registry input StateField registry
     * @param offset control task offset
     */
    GNC_a(StateFieldRegistry &registry, unsigned int offset);

    /**
    * @brief Gets inputs from the ADCS box and dumps them into the state
    * fields listed below.
    */
    void execute() override;

protected:

    InternalStateField<unsigned char>* mission_mode_fp;
    InternalStateField<lin::Vector3f>* omega_vec_fp;
    InternalStateField<lin::Vector3f>* acc_vec_fp;
    InternalStateField<lin::Vector3f>* lin_acc_vec_fp;
    InternalStateField<lin::Vector3f>* acc_error_fp;
    InternalStateField<lin::Vector3f>* euler_vec_fp;
    InternalStateField<lin::Vector3f>* grav_vec_fp;
    InternalStateField<lin::Vector4d>* quat_fp;
    InternalStateField<lin::Vector3f>* mag_vec_fp;
    InternalStateField<lin::Vector4d>* init_quat_dp;
    InternalStateField<float>* altitude_fp;
    InternalStateField<float>* ground_level_fp;
    InternalStateField<lin::Vector2f>* lat_long_fp;
    InternalStateField<lin::Vector2f>* init_lat_long_fp;
    InternalStateField<unsigned char>* fix_qual_fp;
    InternalStateField<double>* init_global_roll_dp;
    InternalStateField<double>* velocity_bmp_dp;
    InternalStateField<lin::Vector3d>* euler_deg_p;





    /**
    * @brief Outputs of GNC_a
    */
    InternalStateField<lin::Vector4f> fin_commands_f;
    InternalStateField<lin::Vector3f> glob_acc_vec_f;
    InternalStateField<lin::Vector2f> thrust_commands_f;
    InternalStateField<lin::Vector3d> setpoint_d;
    InternalStateField<lin::Vector3d> velocity_d;
    InternalStateField<lin::Vector3d> position_d;
    InternalStateField<lin::Vector4d> net_quat_d;
    InternalStateField<lin::Vector3d> glob_pos_err_d;
    InternalStateField<lin::Vector2d> body_pos_err_d;
    InternalStateField<lin::Vector2d> body_velocity_d;
    InternalStateField<double> roll_integral_d;
    InternalStateField<double> pitch_integral_d;
    InternalStateField<double> yaw_integral_d;
    InternalStateField<double> x_integral_d;
    InternalStateField<lin::Vector3d> a_com_d;
    InternalStateField<lin::Matrix2x2d> P_x;
    InternalStateField<lin::Matrix2x2d> P_y;
    InternalStateField<lin::Matrix2x2d> P_z;








    
    // eventually not needed, just was for debug
    float inc_dir = 0;

    // not real control laws, just cool
    void tvc();

    
};

#endif
