#ifndef IMU_MONITOR_HPP_
#define IMU_MONITOR_HPP_
#pragma once

#include "TimedControlTask.hpp"

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
//#include <utility/imumaths.h>

/**
* @brief Gets inputs from the ADCS box and dumps them into the state
* fields listed below.
*/
class IMUMonitor : public TimedControlTask<void>
{
public:
    /**
     * @brief Construct a new ADCSBoxMonitor control task
     * 
     * @param registry input StateField registry
     * @param offset control task offset
     * @param _imu the input adcs system
     */
    //IMUMonitor(StateFieldRegistry &registry, unsigned int offset, Adafruit_BNO055& _imu);
    IMUMonitor(StateFieldRegistry &registry, unsigned int offset);

    /** ADCS Driver. **/
    //Devices::ADCS& adcs_system;
    //Adafruit_BNO055& imu;
    Adafruit_BNO055 imu = Adafruit_BNO055(55, 0x28);

    /**
    * @brief Gets inputs from the ADCS box and dumps them into the state
    * fields listed below.
    */
    void execute() override;

protected:
    /**
    * @brief Inputs to get from ADCS box.
    */

    //! IMU Read Statefields, Internal float for now
    //InternalStateField<f_vector_t> euler_angles;

    //imu sensor event
    //InternalStateField<sensors_event_t> imu_sensor_event;

    InternalStateField<bool> functional_f;

    /**
     * @brief Calibration statuses
     * 
     */
    InternalStateField<unsigned char> sys_cal;
    InternalStateField<unsigned char> gyro_cal;
    InternalStateField<unsigned char> accel_cal;
    InternalStateField<unsigned char> mag_cal;

    // InternalStateField<f_vector_t> 
    //     //linear_acc_vec does not include gravity
    //     linear_acc_vec_f,
    //     //acc_vec includes gravity
    //     acc_vec_f,
    //     //gravity vector
    //     grav_vec_f,
    //     //orientation in euler angles
    //     euler_vec_f,
    //     //gyroscope, angular acceleration vector
    //     gyr_vec_f,
    //     //magnetometer vector
    //     mag_vec_f;
    
    InternalStateField<lin::Vector3f> 
        //linear_acc_vec does not include gravity
        linear_acc_vec_f,
        //acc_vec includes gravity
        acc_vec_f,
        //gravity vector
        grav_vec_f,
        //orientation in euler angles
        euler_vec_f,
        //gyroscope, angular acceleration vector
        gyr_vec_f,
        //magnetometer vector
        mag_vec_f;

    // quaternion
    InternalStateField<lin::Vector4d> quat_f;
    InternalStateField<lin::Vector4d> quat_inv_f;


};

#endif
