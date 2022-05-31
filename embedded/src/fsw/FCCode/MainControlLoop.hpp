#ifndef MAIN_CONTROL_LOOP_TASK_HPP_
#define MAIN_CONTROL_LOOP_TASK_HPP_

#include "ControlTask.hpp"
#include <common/StateField.hpp>
#include <common/StateFieldRegistry.hpp>

#include "ClockManager.hpp"
#include "FieldCreatorTask.hpp"
#include "IMUMonitor.hpp"
#include "BMPMonitor.hpp"
#include "GPSMonitor.hpp"

#include "LEDControlTask.hpp"
#include "MissionManager.hpp"
#include "MissionManager_a.hpp"
#include "DownlinkControlTask.hpp"
#include "GNC.hpp"
#include "GNC_a.hpp"
#include "ServoControlTask.hpp"
#include "MotorControlTask.hpp"
#include "SDCardControlTask.hpp"

class MainControlLoop : public ControlTask<void> {
   protected:
    FieldCreatorTask field_creator_task;
    ClockManager clock_manager;

    //Adafruit_BNO055 imu;
    IMUMonitor imu_monitor;

    Adafruit_BMP280 bmp;
    BMPMonitor bmp_monitor;
    GPSMonitor gps_monitor;

    //Commented Out Stuff for full launch
    //MissionManager mission_manager;
    //GNC gnc;

    //Starhopper Stuff
    MissionManager_a mission_manager_a;
    GNC_a gnc_a;

    ServoControlTask servo_controller;
    MotorControlTask motor_controller;
    DownlinkControlTask downlink_control_task;
    SDCardControlTask sd_card_control_task;
    LEDControlTask led_control_task;

    // Control cycle time offsets, in microseconds
    #ifdef FUNCTIONAL_TEST
    // https://cornellprod-my.sharepoint.com/:x:/r/personal/saa243_cornell_edu/_layouts/15/Doc.aspx?sourcedoc=%7B04C55BBB-7AED-410B-AC43-67352393D6D5%7D&file=Flight%20Software%20Cycle.xlsx&action=default&mobileredirect=true&cid=e2b9bd89-7037-47bf-ad2a-fd8b25808939
        static constexpr unsigned int debug_task_offset          =   3000;
        static constexpr unsigned int piksi_control_task_offset  =   4000;
        static constexpr unsigned int imu_monitor_offset         =   5000;
        static constexpr unsigned int bmp_monitor_offset         =   6000;
        static constexpr unsigned int mission_manager_offset     =  10000;
        static constexpr unsigned int gnc_offset                 =  11000;
        static constexpr unsigned int servo_ct_offset            =  12000;
        static constexpr unsigned int motor_ct_offset            =  13000;
        static constexpr unsigned int downlink_ct_offset         =  14000;
        static constexpr unsigned int led_control_task_offset    =  15000;
    #else
        // static constexpr unsigned int debug_task_offset          =   3000;
        // static constexpr unsigned int piksi_control_task_offset  =   4000;
        // static constexpr unsigned int imu_monitor_offset         =   5000;
        // static constexpr unsigned int bmp_monitor_offset         =   6000;
        // static constexpr unsigned int mission_manager_offset     =  10000;
        // static constexpr unsigned int gnc_offset                 =  11000;
        // static constexpr unsigned int servo_ct_offset            =  12000;
        // static constexpr unsigned int downlink_ct_offset         =  13000;
        // static constexpr unsigned int led_control_task_offset    =  15000;

        // static constexpr unsigned int debug_task_offset          =   0;
        // static constexpr unsigned int piksi_control_task_offset  =   1000;
        // static constexpr unsigned int imu_monitor_offset         =   2000;
        // static constexpr unsigned int bmp_monitor_offset         =   3000;
        // static constexpr unsigned int mission_manager_offset     =   4000;
        // static constexpr unsigned int gnc_offset                 =   5000;
        // static constexpr unsigned int servo_ct_offset            =   6000;
        // static constexpr unsigned int downlink_ct_offset         =   7000;
        // static constexpr unsigned int led_control_task_offset    =   8000;    

        static constexpr unsigned int debug_task_offset          =   0;
        static constexpr unsigned int piksi_control_task_offset  =   1;
        static constexpr unsigned int imu_monitor_offset         =   2;
        static constexpr unsigned int bmp_monitor_offset         =   3;
        static constexpr unsigned int gps_monitor_offset         =   4;
        static constexpr unsigned int mission_manager_offset     =   5;
        static constexpr unsigned int gnc_offset                 =   6;
        static constexpr unsigned int servo_ct_offset            =   7;
        static constexpr unsigned int motor_ct_offset            =   8;
        static constexpr unsigned int downlink_ct_offset         =   9;
        static constexpr unsigned int sd_card_control_task_offset=   10;
        static constexpr unsigned int led_control_task_offset    =   11;

        
    #endif

    /**
     * @brief Total memory use, in bytes.
     */

   public:
    /*
     * @brief Construct a new Main Control Loop Task object
     * 
     * @param registry State field registry
     * @param flow_data Metadata for telemetry flows.
     */
    MainControlLoop(StateFieldRegistry& registry);

    /**
     * @brief Processes state field commands present in the serial buffer.
     */
    void execute() override;

};

#endif