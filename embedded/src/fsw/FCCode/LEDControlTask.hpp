#ifndef LED_CONTROL_TASK_HPP_
#define LED_CONTROL_TASK_HPP_
#pragma once

#include "TimedControlTask.hpp"

/**
* @brief Gets inputs from the ADCS box and dumps them into the state
* fields listed below.
*/
class LEDControlTask : public TimedControlTask<void>
{
public:
    /**
     * @brief Construct a new ADCSBoxMonitor control task
     * 
     * @param registry input StateField registry
     * @param offset control task offset
     */
    LEDControlTask(StateFieldRegistry &registry, unsigned int offset);

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

 
};

#endif
