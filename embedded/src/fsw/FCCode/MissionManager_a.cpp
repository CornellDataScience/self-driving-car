#include "MissionManager_a.hpp"

MissionManager_a::MissionManager_a(StateFieldRegistry& registry, unsigned int offset) :
    TimedControlTask<void>(registry, "mission_ct", offset),
    mission_mode_f("ls.mode"),
    acc_error_f("ls.acc_error"),
    init_quat_d("ls.init_quat"),
    euler_deg("ls.euler_deg"),
    init_lat_long_f("ls.init_coord"),
    ground_level_f("ls.ground_level"),
    engine_on_f("ls.engine_on"),
    servo_on_f("ls.servo_on"),
    agl_alt_f("ls.agl"),
    count("ls.count"),
    init_global_roll("ls.glob_roll")
{
    add_internal_field(mission_mode_f);
    add_internal_field(acc_error_f);
    add_internal_field(init_quat_d);
    add_internal_field(euler_deg);
    add_internal_field(init_lat_long_f);
    add_internal_field(ground_level_f);
    add_internal_field(engine_on_f);
    add_internal_field(servo_on_f);
    add_internal_field(agl_alt_f);
    add_internal_field(count);
    add_internal_field(init_global_roll);

    alt_fp = find_internal_field<float>("bmp.altitude", __FILE__, __LINE__);
    acc_vec_fp = find_internal_field<lin::Vector3f>("imu.acc_vec", __FILE__, __LINE__);
    lat_long_fp = find_internal_field<lin::Vector2f>("gps.lat_long", __FILE__, __LINE__);
    quat_fp = find_internal_field<lin::Vector4d>("imu.quat", __FILE__, __LINE__);
    lin_acc_vec_fp = find_internal_field<lin::Vector3f>("imu.linear_acc_vec", __FILE__, __LINE__);
    omega_vec_fp = find_internal_field<lin::Vector3f>("imu.gyr_vec", __FILE__, __LINE__);
    mag_vec_fp = find_internal_field<lin::Vector3f>("imu.mag_vec", __FILE__, __LINE__);
    sys_cal = find_internal_field<unsigned char>("imu.sys_cal", __FILE__, __LINE__);
    gyro_cal = find_internal_field<unsigned char>("imu.gyro_cal", __FILE__, __LINE__);
    accel_cal = find_internal_field<unsigned char>("imu.accel_cal", __FILE__, __LINE__);
    mag_cal = find_internal_field<unsigned char>("imu.mag_cal", __FILE__, __LINE__);
    
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

void MissionManager_a::execute() {
    mission_mode_t mode = static_cast<mission_mode_t>(mission_mode_f.get());

    calibrate_data();
    switch(mode) {
        case mission_mode_t::warmup:
            Serial.println("Warmup"); ///////////////////////////////////
            dispatch_warmup();
            break;
        case mission_mode_t::pause:
            Serial.println("Pause"); ///////////////////////////////////
            pause();
            break;
        case mission_mode_t::initialization:
            Serial.println("Initialization      "); ///////////////////////////////////
            dispatch_initialization();
            break;
        case mission_mode_t::flight:
            //Serial.print("Starhopper1      ");
            tvc();
            break;
        case mission_mode_t::descent:
            //Serial.print("Starhopper2      ");
            tvc();
            break;
        case mission_mode_t::landed:
            Serial.print("Landed"); ///////////////////////////////////
            dispatch_landed();
            break;
        default:
            printf(debug_severity::error, "Master state not defined: %d\n", static_cast<unsigned int>(mode));
            mission_mode_f.set(static_cast<unsigned char>(mission_mode_t::landed));
            break;
    }
}

void MissionManager_a::set_mission_mode(mission_mode_t mode){
    mission_mode_f.set(static_cast<unsigned char>(mode));
}
void MissionManager_a::calibrate_data(){

    agl_alt_f.set(alt_fp->get() - ground_level_f.get());
    

}
void MissionManager_a::dispatch_warmup() {

    unsigned char calibration_sum = sys_cal->get() + accel_cal->get() + gyro_cal->get() + mag_cal->get();

    
    DebugSERIAL.print("Accelerometer: ");
    DebugSERIAL.print(accel_cal->get());
    DebugSERIAL.print("     Magnometer: ");
    DebugSERIAL.print(mag_cal->get());
    DebugSERIAL.print("     Gyroscope: ");
    DebugSERIAL.print(gyro_cal->get());
    

    // if 5 sec elapse go to init
    // AND ALSO CHECK THAT ALL SENSORS HAVE HIT 3,3,3,3 calibration
    #ifdef WARMUP_CALI
    if(millis() > MM::warmup_millis && calibration_sum == 12){
    #else
    
    if(calibration_sum==12){
    #endif
        pause_ccno = control_cycle_count;
        set_mission_mode(mission_mode_t::pause);
    }
    calibration_sum += 1; // to avoid "unused error", ignore this line
}


void MissionManager_a::pause() {
    if(control_cycle_count-pause_ccno>=MM::pause_cycles){
        enter_init_ccno = control_cycle_count;
        set_mission_mode(mission_mode_t::initialization);
    }
}

void MissionManager_a::dispatch_initialization() {

    // weight the current altitude readings to get a zero value for altitude
    ground_level_f.set(ground_level_f.get() + alt_fp->get() / MM::init_cycles);

    // Gets the offset in each axis for acceleration
    acc_error_f.set( acc_error_f.get() + lin_acc_vec_fp->get() / MM::init_cycles);

    /*
    Serial.print("(");
    Serial.print(acc_error_f.get()(0));
    Serial.print(",");
    Serial.print(acc_error_f.get()(1));
    Serial.print(",");
    Serial.print(acc_error_f.get()(2));
    Serial.println(")");
    */


   //Averages Orientations to get a value for the "equilibrium quaternion"
    init_quat_d.set( init_quat_d.get() + quat_fp->get() / MM::init_cycles);
    double quat_norm=lin::norm(init_quat_d.get());
    init_quat_d.set({
        init_quat_d.get()(0)/quat_norm,
        init_quat_d.get()(1)/quat_norm,
        init_quat_d.get()(2)/quat_norm,
        init_quat_d.get()(3)/quat_norm,
    });


    //Averages current position. Only includes values in average which are in the Albany Region.
    //Uses statefield count to keep track of the number of valid datapoints for averaging
    init_lat_long_f.set(init_lat_long_f.get()+lat_long_fp->get()/MM::init_cycles);

    /*
    float lat = lat_long_fp->get()(0);
    float lon = lat_long_fp->get()(1);
    
    if (lat>42 && lat<43 && lon>-74 && lon<-73){
        count.set(count.get()+1);

        init_lat_long_f.set({
            init_lat_long_f.get()(0)+lat_long_fp->get()(0),
            init_lat_long_f.get()(1)+lat_long_fp->get()(1)
        });

        Serial.println(count.get());
    }
    */

    //Finds initial heading in the Earth's Magnetic field (angle measure from Global North)
    //Since rocket is vertical, it only uses readings in the y and z axes

    
    double m_y = mag_vec_fp->get()(1);
    double m_z = mag_vec_fp->get()(2);
    double roll = (180.0/PI) * atan2(-m_y,-m_z);
    init_global_roll.set(init_global_roll.get()+roll/MM::init_cycles);

    if(control_cycle_count - enter_init_ccno >= MM::init_cycles){
        //Performs final division necessary for position averaging
        /*
        init_lat_long_f.set({
            init_lat_long_f.get()(0)/count.get(),
            init_lat_long_f.get()(1)/count.get()
        });
        */

        enter_flight_millis = millis();
        set_mission_mode(mission_mode_t::flight);
        servo_on_f.set(true);
        engine_on_f.set(true);
    }
}


void MissionManager_a::tvc() {
    float altitude = agl_alt_f.get();

    //If time exceeds flight time, the mission mode is set to descent
    if(millis()-enter_flight_millis> MM::flight_millis){
        set_mission_mode(mission_mode_t::descent);
    }

    Serial.print(lin_acc_vec_fp->get()(0)-acc_error_f.get()(0));
    //Time, attitude, acceleration, and altitude based FTS. 
    //If rocket is in descent and body vertical acceleration exceeds a limit (indicating ground contact), engines are cut
    
    mission_mode_t mode = static_cast<mission_mode_t>(mission_mode_f.get());
    double x_acc = lin_acc_vec_fp->get()(0)-acc_error_f.get()(0);


    if(millis()-enter_flight_millis > MM::FTS_millis || euler_deg.get()(1)>MM::FTS_angle || euler_deg.get()(2)>MM::FTS_angle || altitude>MM::FTS_altitude || (mode==mission_mode_t::descent && abs(x_acc)>MM::FTS_acc)){
        set_mission_mode(mission_mode_t::landed);
    }
}


void MissionManager_a::dispatch_landed() {
    //dump data from registry to SD Card
    // safe vehicle

    servo_on_f.set(false);
    engine_on_f.set(false);
}

