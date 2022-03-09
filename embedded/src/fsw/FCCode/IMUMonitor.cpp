#include "IMUMonitor.hpp"

IMUMonitor::IMUMonitor(StateFieldRegistry &registry, 
    unsigned int offset)
    : TimedControlTask<void>(registry, "imu_monitor", offset),
    //imu(_imu),
    functional_f("imu.functional"),
    sys_cal("imu.sys_cal"),
    gyro_cal("imu.gyro_cal"),
    accel_cal("imu.accel_cal"),
    mag_cal("imu.mag_cal"),
    linear_acc_vec_f("imu.linear_acc_vec"),
    acc_vec_f("imu.acc_vec"),
    grav_vec_f("imu.grav_vec"),
    euler_vec_f("imu.euler_vec"),
    gyr_vec_f("imu.gyr_vec"),
    mag_vec_f("imu.mag_vec"),
    quat_f("imu.quat"),
    quat_inv_f("imu.quat_inv")
    {
        //add statefields to registry
        add_internal_field(functional_f);
        add_internal_field(linear_acc_vec_f);
        add_internal_field(acc_vec_f);
        add_internal_field(grav_vec_f);
        add_internal_field(euler_vec_f);
        add_internal_field(gyr_vec_f);
        add_internal_field(mag_vec_f);
        add_internal_field(quat_f);
        add_internal_field(quat_inv_f);


        add_internal_field(sys_cal);
        add_internal_field(gyro_cal);
        add_internal_field(accel_cal);
        add_internal_field(mag_cal);

        // /** Remap Axis Settings to P5 per the BNO055 spec. */
        // imu.setAxisRemap(Adafruit_BNO055::adafruit_bno055_axis_remap_config_t::REMAP_CONFIG_P5);
        // imu.setAxisSign(Adafruit_BNO055::adafruit_bno055_axis_remap_sign_t::REMAP_SIGN_P5);

        //imu = Adafruit_BNO055(55, 0x28);
        //set up imu?
        if(!imu.begin()){
            //debug print
            functional_f.set(false);
        }
        else
        {
            functional_f.set(true);
        }

        // absolute fusion mode
        imu.setMode(Adafruit_BNO055::adafruit_bno055_opmode_t::OPERATION_MODE_NDOF);


        /** Remap Axis Settings to P1 per the BNO055 spec. */
        imu.setAxisRemap(Adafruit_BNO055::adafruit_bno055_axis_remap_config_t::REMAP_CONFIG_P1);
        imu.setAxisSign(Adafruit_BNO055::adafruit_bno055_axis_remap_sign_t::REMAP_SIGN_P1);
        
        #ifdef LOAD_CALI
        /** Load a specific set of sensor offsets */
        unsigned char offsets[22] = {242,255,214,255,243,255,250,254,0,255,105,0,255,255,1,0,255,255,232,3,146,2}; // calibrated from scao imu @ 06/14
        imu.setSensorOffsets(offsets);
        #endif
        // set mode just in case
        imu.setMode(Adafruit_BNO055::adafruit_bno055_opmode_t::OPERATION_MODE_NDOF);

        // NOT NECESSARY MODIFY SHIHAO FORK IF DEFAULT INITIALIZATION IS REQUIRED

        /* Use external crystal for better accuracy */
        imu.setExtCrystalUse(true);
    }

void IMUMonitor::execute(){

    //linear_acc_vec is acceleration without gravity
    sensors_event_t linear_acc_vec,
        //acc_vec includes gravity
        acc_vec,
        //gravity vector
        grav_vec,
        //orientation in euler angles
        euler_vec,
        //gyroscope, angular acceleration vector
        gyr_vec,
        //magnetometer vector
        mag_vec;

    //poll actual i2c device, and fill containers
    imu.getEvent(&linear_acc_vec, Adafruit_BNO055::VECTOR_LINEARACCEL);
    imu.getEvent(&acc_vec, Adafruit_BNO055::VECTOR_ACCELEROMETER);
    imu.getEvent(&grav_vec, Adafruit_BNO055::VECTOR_GRAVITY);
    imu.getEvent(&euler_vec, Adafruit_BNO055::VECTOR_EULER);
    imu.getEvent(&gyr_vec, Adafruit_BNO055::VECTOR_GYROSCOPE);
    imu.getEvent(&mag_vec, Adafruit_BNO055::VECTOR_MAGNETOMETER);

    // temp calibration containers
    unsigned char s, g, a, m;
    imu.getCalibration(&s, &g, &a, &m);
    sys_cal.set(s);
    gyro_cal.set(g);
    accel_cal.set(a);
    mag_cal.set(m);


    // Serial1.print(sys_stat);
    // Serial1.print(",");
    // Serial1.print(gyro_stat);
    // Serial1.print(",");

    // Serial1.print(accel_stat);
    // Serial1.print(",");

    // Serial1.print(mag_stat);
    // Serial1.print("\n");


    //poll for quatnernion
    imu::Quaternion local_quat = imu.getQuat();

    //IF THIS IS TOO SLOW, DELETE READ OPERATIONS OF ^VECTORS WE DON'T NEED

    //IF BELOW TOO SLOW, STOP USING SENSOR EVENTS YIKES
    //dump temporary containers into statefields

    // lin::Vector3f v1{
    //     linear_acc_vec.acceleration.x, 
    //     linear_acc_vec.acceleration.y, 
    //     linear_acc_vec.acceleration.z};
    // linear_acc_vec_f.set({
    //     linear_acc_vec.acceleration.x, 
    //     linear_acc_vec.acceleration.y, 
    //     linear_acc_vec.acceleration.z});

    // OLD STD ARRAY VECTORS:

    linear_acc_vec_f.set({
        linear_acc_vec.acceleration.x, 
        linear_acc_vec.acceleration.y, 
        linear_acc_vec.acceleration.z});

    acc_vec_f.set({
        acc_vec.acceleration.x, 
        acc_vec.acceleration.y, 
        acc_vec.acceleration.z
    });

    grav_vec_f.set({
        grav_vec.acceleration.x,
        grav_vec.acceleration.y,
        grav_vec.acceleration.z
    });

    euler_vec_f.set({
        euler_vec.orientation.x,
        euler_vec.orientation.y,
        euler_vec.orientation.z,
    });
    
    gyr_vec_f.set({
        gyr_vec.gyro.x,
        gyr_vec.gyro.y,
        gyr_vec.gyro.z,
    });

    mag_vec_f.set({
        mag_vec.magnetic.x,
        mag_vec.magnetic.y,
        mag_vec.magnetic.z
    });

    //Experimenting with Global Heading (Using Magnetometer)
    /*
    DebugSERIAL.print(m);
    DebugSERIAL.print("(");
    DebugSERIAL.print(mag_vec_f.get()(0));
    DebugSERIAL.print(",");
    DebugSERIAL.print(mag_vec_f.get()(1));
    DebugSERIAL.print(",");
    DebugSERIAL.print(mag_vec_f.get()(2));
    DebugSERIAL.print(")  ");
    DebugSERIAL.print(sqrt(mag_vec_f.get()(1)*mag_vec_f.get()(1)+mag_vec_f.get()(2)*mag_vec_f.get()(2)));
    DebugSERIAL.print("  ");
    DebugSERIAL.println((180.0/PI)*atan2(-mag_vec_f.get()(1),-mag_vec_f.get()(2)));
    */

    quat_f.set({
        local_quat.w(),
        local_quat.x(),
        local_quat.y(),
        local_quat.z(),
        
    });

    quat_inv_f.set({
        local_quat.w(),
        -local_quat.x(),
        -local_quat.y(),
        -local_quat.z(), 
    });
}