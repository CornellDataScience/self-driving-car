#include "MainControlLoop.hpp"
#include "constants.hpp"


MainControlLoop::MainControlLoop(StateFieldRegistry& registry)
    : ControlTask<void>(registry), 
      field_creator_task(registry),
      clock_manager(registry, PAN::control_cycle_time),
      imu_monitor(registry, imu_monitor_offset),
      bmp_monitor(registry, bmp_monitor_offset),
      gps_monitor(registry, gps_monitor_offset),

      //mission_manager(registry, mission_manager_offset),
      //gnc(registry, gnc_offset),
      
      mission_manager_a(registry, mission_manager_offset),
      gnc_a(registry, gnc_offset),
      servo_controller(registry, servo_ct_offset),
      motor_controller(registry,motor_ct_offset),
      downlink_control_task(registry, downlink_ct_offset),
      sd_card_control_task(registry, sd_card_control_task_offset),
      led_control_task(registry, led_control_task_offset)

 // This item is initialized last so it has access to all state fields
{
    delay(1000); //necessary for imu warm-up
}

void MainControlLoop::execute() {
    clock_manager.execute();
    imu_monitor.execute_on_time();
    bmp_monitor.execute_on_time();
    //gps_monitor.execute_on_time();

    /*
    mission_manager.execute_on_time();
    gnc.execute_on_time();
    */

    mission_manager_a.execute_on_time();
    gnc_a.execute_on_time();
    #ifndef STATIC
    servo_controller.execute_on_time();
    #endif
    motor_controller.execute_on_time();
    #ifndef DL_OFF
    downlink_control_task.execute_on_time();
    #endif
    sd_card_control_task.execute_on_time();
    led_control_task.execute_on_time();
    
}