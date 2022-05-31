#ifndef DOWNLINK_CONTROL_TASK_HPP_
#define DOWNLINK_CONTROL_TASK_HPP_
#pragma once

#include "TimedControlTask.hpp"
#include "constants.hpp"
/**
* @brief Gets inputs from the ADCS box and dumps them into the state
* fields listed below.
*/
class DownlinkControlTask : public TimedControlTask<void>
{
public:
    /**
     * @brief Construct a new ADCSBoxMonitor control task
     * 
     * @param registry input StateField registry
     * @param offset control task offset
     */
    DownlinkControlTask(StateFieldRegistry &registry, unsigned int offset);

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
    //InternalStateField<lin::Vector3f> euler_angles;

    //imu sensor event
    //InternalStateField<sensors_event_t> imu_sensor_event;

    InternalStateField<float>* altitude_fp;
    InternalStateField<float>* agl_alt_fp;
    InternalStateField<unsigned char>* mm_fp;
    InternalStateField<lin::Vector3f>* linear_acc_fp;
    InternalStateField<lin::Vector3f>* euler_fp;
    InternalStateField<lin::Vector3f>* acc_fp;
    InternalStateField<lin::Vector3f>* gyr_fp;
    InternalStateField<lin::Vector4d>* quat_fp;

    // helper functions for debug out
    template<typename T, size_t N>
    void telem_compact(std::array<T, N>& array){
        for(size_t i = 0; i < N-1; i++){
            telem_element(array[i]);
            TelemSERIAL.print(",");
        }
        telem_element(array[N-1]);
        TelemSERIAL.print(";");
    }

    template<typename T, size_t N>
    void telem_compact(lin::Vector<T, N>& array){
        for(size_t i = 0; i < N-1; i++){
            telem_element(array(i));
            TelemSERIAL.print(",");
        }
        telem_element(array(N-1));
        TelemSERIAL.print(";");
    }

    template<typename T>
    void telem_element(T element){
        if(std::is_same<T, float>::value || std::is_same<T, double>::value)
            TelemSERIAL.printf("%g", element);
        else if(std::is_same<T, unsigned char>::value || std::is_same<T, unsigned int>::value)
            TelemSERIAL.printf("%u", element);
        else if(std::is_same<T, char>::value || std::is_same<T, int>::value)
            TelemSERIAL.printf("%d", element);
        else
            TelemSERIAL.print("[ERROR] UNEXPECTED ELEMENT TYPE.");
    }

    template<typename T>
    void telem_solo(T element){
        telem_element(element);
        TelemSERIAL.print(";");
    }    
};

#endif
