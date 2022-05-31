#ifndef MISSION_MANAGER_HPP_
#define MISSION_MANAGER_HPP_

#include "TimedControlTask.hpp"

#include "mission_mode_t.enum"
#include "adcs_mode_t.enum"

class MissionManager : public TimedControlTask<void> {
    public:

        MissionManager(StateFieldRegistry& registry, unsigned int offset);
    
        void execute() override;

    protected:

        void set_mission_mode(mission_mode_t mode);

        void calibrate_data();

        void dispatch_warmup();
        void dispatch_initialization();
        void dispatch_standby();
        void dispatch_detumble();
        void dispatch_bellyflop();
        void dispatch_landed();

        // Fields that control overall mission state.
        /**
         * @brief Current mission mode (see mission_mode_t.enum)
         */
        InternalStateField<unsigned char> mission_mode_f;
        InternalStateField<float> ground_level_f;
        InternalStateField<bool> engine_on_f;
        InternalStateField<bool> servo_on_f;
        InternalStateField<float> agl_alt_f;



        InternalStateField<float>* alt_fp;
        InternalStateField<lin::Vector3f>* acc_vec_fp;
        InternalStateField<lin::Vector3f>* omega_vec_fp;

        long enter_init_millis;
        int enter_init_ccno;
        int enter_freefall_cnno;
        long enter_bellyflop_millis;
        // long enter_standby_millis;
};

#endif
