#ifndef CONSTANTS_HPP_
#define CONSTANTS_HPP_

namespace PAN {
    // Environment-based initializations of the control loop time.
    // control_cycle_time is the value actually used for timing. The
    // other constants are just informational.
    constexpr unsigned int control_cycle_time_ms = 100;
    constexpr unsigned int control_cycle_time_us = control_cycle_time_ms * 1000;
    constexpr unsigned int control_cycle_time = control_cycle_time_us;
}

namespace PINOUT {

    // let the GPS be connected to TX and RX 3
    // let the telemetry radio (57600 baud) be connected to TX1 and RX1

    // not actually a member variable, just putting it here
    #define GPSSerial Serial3

    // faster than 9600, hopefully supports 10hz
    constexpr unsigned int gps_serial_baud = 115200;

    #ifdef HARDLINE
    #define TelemSERIAL Serial
    constexpr unsigned int telem_serial_baud = 115200;
    #endif
    #ifdef AIR
    #define TelemSERIAL Serial1
    constexpr unsigned int telem_serial_baud = 57600;
    #endif

    #define DebugSERIAL Serial
}

namespace MM {
    constexpr unsigned int warmup_millis = 10 * 1000;
    constexpr unsigned int init_millis = 10 * 1000;
    constexpr unsigned int acc_millis = 5 * 1000;
    constexpr unsigned int pause_cycles = 170;
    constexpr unsigned int init_cycles = 100;

    //Flight Time Before Descent
    constexpr unsigned int flight_millis = 5 * 1000;


    //Flight Termination time, angle, and altitude
    constexpr unsigned int FTS_millis = 1 * 17 * 1000;
    constexpr float FTS_angle = 60.0;
    constexpr float FTS_altitude = 8.0;
    constexpr float FTS_acc = 5.0;

    /**
     * @brief If measure acceleration is below this threshold, we're in free fall.
     * 
     */
    constexpr float free_fall_thresh = 4.0;

    constexpr unsigned int consectuve_free_fall_cycles = 0;
    
    constexpr float detumble_thresh = 300.0; // rads per sec?
}
/**
 * @brief A set of constants for the Servo CT
 * 
 */
namespace SERVO {
    constexpr unsigned char num_flaps = 4;
    constexpr unsigned char flap1_pin = 2;
    constexpr unsigned char flap2_pin = 3;
    constexpr unsigned char flap3_pin = 35;
    constexpr unsigned char flap4_pin = 36;
    constexpr unsigned char fin1_pin = 3;   //Pitch
    constexpr unsigned char fin2_pin = 22;  //Pitch
    constexpr unsigned char fin3_pin = 2;   //Yaw
    constexpr unsigned char fin4_pin = 23;   //Yaw
    constexpr unsigned char motor1_pin = 29;
    constexpr unsigned char motor2_pin = 30;

    // bounds expected from GNC
    constexpr float servo_cmd_range = 90;
    constexpr float flap_cmd_min = 0;
    constexpr float flap_cmd_max = flap_cmd_min + servo_cmd_range;

    // bounds for the range for servo (limits on write microseconds)
    constexpr float servo_min = 0;
    constexpr float servo_max = 180;

    // how many degrees the servo is actually capable of
    constexpr float actual_range = 180;

    constexpr float servo_center = (servo_max - servo_min)/2.0;

    // range used for actual write microseconds
    constexpr float flap_write_min = servo_center - servo_cmd_range/2.0;
    constexpr float flap_write_max = servo_center + servo_cmd_range/2.0;

}

namespace CONTROLS{
    constexpr lin::Vector3d setpoint_1 {2.5,0.0,0.0}; //Setpoints in the hop
    constexpr lin::Vector3d setpoint_2 {0.0,0.0,0.0}; 



    constexpr double max_position_error = 5.0;
    constexpr double max_tilt = 3.0;
    constexpr double alph_pitch_max=25;
    constexpr double alph_yaw_max=25;
    constexpr double a_x_max=3;
    constexpr double weight=1; //Factor by which attitude control commands thrust
    constexpr double T_max=8.5; //Maximum thrust in Newtons
    constexpr double servo_max=40; //Measured from equilibrium

    //Y and Z gains
    constexpr double Kd_p_tilt = 1.25;
    constexpr double Kd_y_tilt = 1.25;

    //Pitch Gains
    constexpr double Kp_pitch = 1.25;
    constexpr double Ki_pitch = 0;
    constexpr double Kd_pitch = 0.3;

    //Yaw Gains
    constexpr double Kp_yaw = 1.25;
    constexpr double Ki_yaw = 0;
    constexpr double Kd_yaw = 0.3;

    //Roll Gains
    constexpr double Kp_roll = 0.7;
    constexpr double Ki_roll = 0;
    constexpr double Kd_roll = 0.1;

    //Ascent Gains
    constexpr double Kp_xa = 0.4;
    constexpr double Ki_xa = 0;
    constexpr double Kd_xa = 0.1;

    //Landing Gains
    constexpr double Kp_xd = 0.4;
    constexpr double Ki_xd = 0.0;
    constexpr double Kd_xd = 0.1;

    //Thrust Offset
    constexpr int thrust_offset = 530;
    constexpr int landing_offset = 60;

}

#endif
