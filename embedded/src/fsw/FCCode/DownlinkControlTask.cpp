#include "DownlinkControlTask.hpp"

DownlinkControlTask::DownlinkControlTask(StateFieldRegistry &registry, 
    unsigned int offset)
    : TimedControlTask<void>(registry, "downlink_control_task", offset)
    {
        altitude_fp = find_internal_field<float>("bmp.altitude", __FILE__, __LINE__);
        agl_alt_fp = find_internal_field<float>("ls.agl", __FILE__, __LINE__);
        mm_fp = find_internal_field<unsigned char>("ls.mode", __FILE__, __LINE__);
        euler_fp = find_internal_field<lin::Vector3f>("imu.euler_vec", __FILE__, __LINE__);
        acc_fp = find_internal_field<lin::Vector3f>("imu.acc_vec", __FILE__, __LINE__);
        linear_acc_fp = find_internal_field<lin::Vector3f>("imu.linear_acc_vec", __FILE__, __LINE__);
        gyr_fp = find_internal_field<lin::Vector3f>("imu.gyr_vec", __FILE__, __LINE__);
        quat_fp = find_internal_field<lin::Vector4d>("imu.quat", __FILE__, __LINE__);

        TelemSERIAL.begin(PINOUT::telem_serial_baud);

        // just have this for debug availability
        DebugSERIAL.begin(115200);
    }

void DownlinkControlTask::execute(){

    lin::Vector3f linear_acc_read = linear_acc_fp->get();
    lin::Vector3f acc_read = acc_fp->get();
    lin::Vector3f euler_read = euler_fp->get();
    lin::Vector3f gyr_read = gyr_fp->get();
    lin::Vector4d quat_read = quat_fp->get();
    unsigned char mm = mm_fp->get();

    #ifdef AIR_TEST
    TelemSERIAL.print("0000;1111;2222;3333;4444;5555;6666;7777;8888;9999;0000,,,");
    return;
    #endif

    // unsigned int temp = PAN::control_cycle_time;
    #ifdef SPEED_TEST
    TelemSERIAL.printf("CN: %u, CCT: %u\n", control_cycle_count, PAN::control_cycle_time_ms);
    #endif

    #if defined(COMPACT)
    telem_solo(control_cycle_count);
    telem_solo(mm);
    telem_solo(agl_alt_fp->get());
    telem_solo(altitude_fp->get());
    telem_compact(linear_acc_read);
    telem_compact(acc_read);
    telem_compact(euler_read);
    telem_compact(gyr_read);
    telem_compact(quat_read);
    TelemSERIAL.print("\n");
    #endif

    #if defined(FULL_DL)
    TelemSERIAL.printf("Control Cycle Num: %u\n", control_cycle_count);
    telem_solo(mm); // should make nicer
    TelemSERIAL.printf("Altitude (m): %f\n", altitude_fp->get());
    TelemSERIAL.printf("Linear Acc: %f, %f, %f\n", linear_acc_read(0), linear_acc_read(1), linear_acc_read(2));
    TelemSERIAL.printf("Acc: %f, %f, %f\n", acc_read(0), acc_read(1), acc_read(2));
    TelemSERIAL.printf("Euler: %f, %f, %f\n", euler_read(0), euler_read(1), euler_read(2));
    TelemSERIAL.printf("Gyr: %f, %f, %f\n", gyr_read(0), gyr_read(1), gyr_read(2));
    TelemSERIAL.printf("Q: %f, %f, %f, %f\n", quat_read(0), quat_read(1), quat_read(2), quat_read(3));
    TelemSERIAL.print("\n");
    #endif

}