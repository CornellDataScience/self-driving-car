#ifndef MISSION_MANAGER_A_HPP_
#define MISSION_MANAGER_A_HPP_

#include "TimedControlTask.hpp"

#include "mission_mode_t.enum"
#include "adcs_mode_t.enum"

class MissionManager_a : public TimedControlTask<void> {
    public:

        MissionManager_a(StateFieldRegistry& registry, unsigned int offset);
    
        void execute() override;

    protected:

        void set_mission_mode(mission_mode_t mode);

        void calibrate_data();
        void dispatch_warmup();
        void dispatch_initialization();
        void pause();
        void tvc();
        void dispatch_landed();

        // Fields that control overall mission state.
        /**
         * @brief Current mission mode (see mission_mode_t.enum)
         */
        InternalStateField<unsigned char> mission_mode_f;
        InternalStateField<lin::Vector3f> acc_error_f;
        InternalStateField<lin::Vector4d> init_quat_d;
        InternalStateField<lin::Vector3d> euler_deg;
        InternalStateField<lin::Vector2f> init_lat_long_f;
        InternalStateField<float> ground_level_f;
        InternalStateField<bool> engine_on_f;
        InternalStateField<bool> servo_on_f;

        InternalStateField<float> agl_alt_f;        
        InternalStateField<int> count;
        InternalStateField<double> init_global_roll;

        InternalStateField<float>* alt_fp;
        InternalStateField<lin::Vector3f>* acc_vec_fp;
        InternalStateField<lin::Vector4d>* quat_fp;
        InternalStateField<lin::Vector2f>* lat_long_fp;
        InternalStateField<lin::Vector3f>* lin_acc_vec_fp;
        InternalStateField<lin::Vector3f>* omega_vec_fp;
        InternalStateField<lin::Vector3f>* mag_vec_fp;

        InternalStateField<unsigned char>* sys_cal;
        InternalStateField<unsigned char>* gyro_cal;
        InternalStateField<unsigned char>* accel_cal;
        InternalStateField<unsigned char>* mag_cal;

        long enter_init_millis;
        int enter_init_ccno;
        long enter_flight_millis;
        int enter_freefall_cnno;
        int pause_ccno;
        //long enter_bellyflop_millis;
        // long enter_standby_millis;
};

#endif
