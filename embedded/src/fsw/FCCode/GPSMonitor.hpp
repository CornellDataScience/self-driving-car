#ifndef GPS_MONITOR_HPP_
#define GPS_MONITOR_HPP_
#pragma once

#include "TimedControlTask.hpp"

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
//#include <utility/imumaths.h>

#include "constants.hpp"
#include <Adafruit_GPS.h>

/**
* @brief Gets inputs from the ADCS box and dumps them into the state
* fields listed below.
*/
class GPSMonitor : public TimedControlTask<void>
{
public:
    /**
     * @brief Construct a new ADCSBoxMonitor control task
     * 
     * @param registry input StateField registry
     * @param offset control task offset
     * @param _imu the input adcs system
     */
    //GPSMonitor(StateFieldRegistry &registry, unsigned int offset, Adafruit_BNO055& _imu);
    GPSMonitor(StateFieldRegistry &registry, unsigned int offset);

    Adafruit_GPS GPS;

    void update_state_fields();

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
     * @brief True if the GPS has a 3D fix.
     * 
     */
    InternalStateField<bool> has_fix_f;

    /**
     * @brief True iff there is new nmea data that
     * has been parsed correctly.
     * 
     */
    InternalStateField<bool> has_new_nmea_f;
    
    InternalStateField<unsigned char> fix_quality_f;

    /**
     * @brief Contains the most recent lattitude and longitude
     * as decimal degrees
     * 
     * For now, it assumes that you're running this in the USA
     * 
     */
    InternalStateField<lin::Vector2f> lat_long_f;

};

#endif
