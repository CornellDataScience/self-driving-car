#include "BMPMonitor.hpp"
#include <math.h>       /* pow */

BMPMonitor::BMPMonitor(StateFieldRegistry &registry, 
    unsigned int offset)
    : TimedControlTask<void>(registry, "bmp_monitor", offset),
    functional_f("bmp.functional"),
    temp_f("bmp.temp"),
    pressure_f("bmp.pressure"),
    altitude_f("bmp.altitude"),
    velocity_bmp_d("bmp.velocity")
    {
        //add statefields to registry
        add_internal_field(functional_f);
        add_internal_field(temp_f);
        add_internal_field(pressure_f);
        add_internal_field(altitude_f);
        add_internal_field(velocity_bmp_d);

        //set up imu?
        if(!bmp.begin()){
            //debug print
            //TODO THROW ERROR?
            functional_f.set(false);
        }
        else{
            functional_f.set(true);
        }

        /* Default settings from datasheet. */
        bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,     /* Operating Mode. */
                        Adafruit_BMP280::SAMPLING_X2,     /* Temp. oversampling */
                        Adafruit_BMP280::SAMPLING_X16,    /* Pressure oversampling */
                        Adafruit_BMP280::FILTER_X16,      /* Filtering. */
                        Adafruit_BMP280::STANDBY_MS_1); /* Standby time. */

    }

void BMPMonitor::execute(){

    //linear_acc_vec is acceleration without gravity
    sensors_event_t
        // temperature
        temp,
        // pressure
        pressure;

    // poll sensor pointers
    bmp_temp->getEvent(&temp);
    bmp_pressure->getEvent(&pressure);

    float temp_float = temp.temperature;
    float pressure_float = pressure.pressure * hPa_to_Pa;

    //dump temporary containers into statefields
    temp_f.set(temp_float);
    pressure_f.set(pressure_float);

    //consider just locking in temperature
    float temp_K_float = temp_float + C_to_K;
    float exponent = g_0 * big_M / (R_star * L_b);
    float altitude_float = (temp_K_float / L_b) * (pow((pressure_float / P_b), -1.0f/exponent) - 1.0f) + h_b;

    velocity_bmp_d.set(1.0*(altitude_float-altitude_f.get())/(PAN::control_cycle_time_ms/1000.0));
    altitude_f.set(altitude_float);




}