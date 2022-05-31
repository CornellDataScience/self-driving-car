#ifndef BMP_MONITOR_HPP_
#define BMP_MONITOR_HPP_
#pragma once

#include "TimedControlTask.hpp"

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP280.h>

/**
* @brief Gets inputs from the BMP280 and dumps them into the state
* fields listed below.
*/
class BMPMonitor : public TimedControlTask<void>
{
public:
    /**
     * @brief Construct a new ADCSBoxMonitor control task
     * 
     * @param registry input StateField registry
     * @param offset control task offset
     * @param _bmp the BMP280 driver object reference
     */
    BMPMonitor(StateFieldRegistry &registry, unsigned int offset);

    //hPa to Pa conversion
    static constexpr float hPa_to_Pa = 100.0;

    /** Static pressure at sea level */
    static constexpr float P_b = 101325.0;

    /** Temperature lapse rate */
    static constexpr float L_b = -0.0065;

    /** Reference level for layer, we're always below 11000 m for lodestar lol */
    static constexpr float h_b = 0.0;

    /** Adjusted gas constant, see wikipedia */
    static constexpr float R_star = 8.3144598;

    /** gravity */
    static constexpr float g_0 = 9.80665;

    /** molar mass of Earth's air */
    static constexpr float big_M = 0.0289644;

    /** C to K offset */
    static constexpr float C_to_K = 273.15; 

    /** BMP280 device */
    Adafruit_BMP280 bmp;
    Adafruit_Sensor *bmp_temp = bmp.getTemperatureSensor();
    Adafruit_Sensor *bmp_pressure = bmp.getPressureSensor();

    /**
    * @brief Gets inputs from the BMP280 and dumps them into the state
    * fields listed below.
    */
    void execute() override;

protected:

    InternalStateField<bool> functional_f;

    /**
    * @brief Inputs to get from BMP280
    * 
    * temp in degrees Celcius
    * pressure in hPa
    */
    InternalStateField<float>
        /** temperature state field in degrees Celcius */
        temp_f, 
        /** pressure state field */
        pressure_f,
        /** altitude statefield */
        altitude_f;
    InternalStateField<double> velocity_bmp_d;
 };

#endif
