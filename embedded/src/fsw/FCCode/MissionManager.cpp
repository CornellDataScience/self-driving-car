#include "MissionManager.hpp"

MissionManager::MissionManager(StateFieldRegistry& registry, unsigned int offset) :
    TimedControlTask<void>(registry, "mission_ct", offset),
    mission_mode_f("ls.mode"),
    ground_level_f("ls.ground_level"),
    engine_on_f("ls.engine_on"),
    servo_on_f("ls.servo_on"),
    agl_alt_f("ls.agl")
{
    add_internal_field(mission_mode_f);
    add_internal_field(ground_level_f);
    add_internal_field(engine_on_f);
    add_internal_field(servo_on_f);
    add_internal_field(agl_alt_f);

    alt_fp = find_internal_field<float>("bmp.altitude", __FILE__, __LINE__);
    acc_vec_fp = find_internal_field<lin::Vector3f>("imu.acc_vec", __FILE__, __LINE__);
    omega_vec_fp = find_internal_field<lin::Vector3f>("imu.gyr_vec", __FILE__, __LINE__);
    
    // adcs_mode_fp = find_writable_field<unsigned char>("adcs.mode", __FILE__, __LINE__);
    // adcs_cmd_attitude_fp = find_writable_field<f_quat_t>("adcs.cmd_attitude", __FILE__, __LINE__);
    // adcs_ang_rate_fp = find_readable_field<float>("adcs.ang_rate", __FILE__, __LINE__);
    // adcs_min_stable_ang_rate_fp = find_writable_field<float>("adcs.min_stable_ang_rate", __FILE__, __LINE__);
    // radio_mode_fp = find_readable_field<unsigned char>("radio.mode", __FILE__, __LINE__);

    mission_mode_f.set(static_cast<unsigned char>(mission_mode_t::warmup));
    ground_level_f.set(0);

    enter_init_ccno = -1;
    enter_freefall_cnno = -1;

    servo_on_f.set(false);
    engine_on_f.set(false);
}

void MissionManager::execute() {
    mission_mode_t mode = static_cast<mission_mode_t>(mission_mode_f.get());

    calibrate_data();

    if(millis() > MM::FTS_millis)
        set_mission_mode(mission_mode_t::landed);

    switch(mode) {
        case mission_mode_t::warmup:
            dispatch_warmup();
            break;
        case mission_mode_t::initialization:
            dispatch_initialization();
            break;
        case mission_mode_t::standby:
            dispatch_standby();
            break;
        case mission_mode_t::detumble:
            dispatch_detumble();
            break;
        case mission_mode_t::bellyflop:
            dispatch_bellyflop();
            break;
        case mission_mode_t::landed:
            dispatch_landed();
            break;
        default:
            printf(debug_severity::error, "Master state not defined: %d\n", static_cast<unsigned int>(mode));
            mission_mode_f.set(static_cast<unsigned char>(mission_mode_t::landed));
            break;
    }
}

void MissionManager::set_mission_mode(mission_mode_t mode){
    mission_mode_f.set(static_cast<unsigned char>(mode));
}
void MissionManager::calibrate_data(){

    agl_alt_f.set(alt_fp->get() - ground_level_f.get());

}
void MissionManager::dispatch_warmup() {
    // if 5 sec elapse go to init
    if(millis() > MM::warmup_millis){
        set_mission_mode(mission_mode_t::initialization);
        enter_init_ccno = control_cycle_count;
    }
}

void MissionManager::dispatch_initialization() {
    // weight the current altitude readings
    ground_level_f.set(ground_level_f.get() + alt_fp->get() / MM::init_cycles);

    if(control_cycle_count - enter_init_ccno >= MM::init_cycles){
        set_mission_mode(mission_mode_t::standby);
        servo_on_f.set(true);
    }
}

void MissionManager::dispatch_standby() {

    float norm = lin::norm(acc_vec_fp->get());
    if(norm < MM::free_fall_thresh){
        if(enter_freefall_cnno == -1)
            enter_freefall_cnno = control_cycle_count;
            
        if(control_cycle_count - enter_freefall_cnno >= MM::consectuve_free_fall_cycles){
            set_mission_mode(mission_mode_t::detumble);
        }
    }
    else
        enter_freefall_cnno = -1;
    // Serial1.printf("%f", norm);
    // Serial1.print("yeet");

}

// lode star needs detumble too. If we're tumbling waaaay to fast, 
// step one should just be to keep fins out to zero out all spin
void MissionManager::dispatch_detumble() {
    
    float omega_norm = lin::norm(omega_vec_fp->get());
    if(omega_norm < MM::detumble_thresh){
        set_mission_mode(mission_mode_t::bellyflop);
    }

}

void MissionManager::dispatch_bellyflop() {
    //servo should already be on

    //actuate as you would during belly flop
}

void MissionManager::dispatch_landed() {
    //dump data from registry to SD Card
    // safe vehicle

    servo_on_f.set(false);
    engine_on_f.set(false);
}

