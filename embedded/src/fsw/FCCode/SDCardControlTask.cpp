#include "SDCardControlTask.hpp"

SDCardControlTask::SDCardControlTask(StateFieldRegistry &registry, 
    unsigned int offset)
    : TimedControlTask<void>(registry, "sd_card_control_task", offset)
    {
        flap_commands_fp = find_internal_field<lin::Vector4f>("gnc.flap_cmds", __FILE__, __LINE__);
        servo_on_fp = find_internal_field<bool>("ls.servo_on", __FILE__, __LINE__);
        fin_commands_fp = find_internal_field<lin::Vector4f>("gnc_a.fin_cmds", __FILE__, __LINE__);
        acc_error_fp = find_internal_field<lin::Vector3f>("ls.acc_error", __FILE__, __LINE__);
        lin_acc_vec_fp = find_internal_field<lin::Vector3f>("imu.linear_acc_vec", __FILE__, __LINE__);
        euler_deg_p = find_internal_field<lin::Vector3d>("ls.euler_deg", __FILE__, __LINE__);
        position_dp = find_internal_field<lin::Vector3d>("gnc_a.position", __FILE__, __LINE__);
        a_com_p = find_internal_field<lin::Vector3d>("gnc_a.a_com", __FILE__, __LINE__);
        thrust_commands_fp = find_internal_field<lin::Vector2f>("gnc_a.thrust_cmds", __FILE__, __LINE__);

        SD.begin(chipSelect);
        myFile = SD.open("data.txt", FILE_WRITE);
        
    }

void SDCardControlTask::execute(){

    if(myFile){
        myFile.printf("------------------------------------------------\n");
        myFile.printf("Control Cycle: %u\n", control_cycle_count);

        myFile.printf("Euler: (");
        myFile.print(euler_deg_p->get()(0));
        myFile.print(",");
        myFile.print(euler_deg_p->get()(1));
        myFile.print(",");
        myFile.print(euler_deg_p->get()(2));
        myFile.print(")\n");

        myFile.printf("Altitude: ");
        myFile.print(position_dp->get()(0));
        myFile.printf("\n");

        myFile.printf("Body Acceleration: (");
        myFile.print(lin_acc_vec_fp->get()(0)-acc_error_fp->get()(0));
        myFile.print(",");
        myFile.print(lin_acc_vec_fp->get()(1)-acc_error_fp->get()(1));
        myFile.print(",");
        myFile.print(lin_acc_vec_fp->get()(2)-acc_error_fp->get()(2));
        myFile.print(")\n");

        myFile.printf("Commanded Accelerations: (");
        myFile.print(a_com_p->get()(0));
        myFile.print(",");
        myFile.print(a_com_p->get()(1));
        myFile.print(",");
        myFile.print(a_com_p->get()(2));
        myFile.print(")\n");

        myFile.printf("Thrust: ");
        myFile.print(4.06*(thrust_commands_fp->get()(0)+thrust_commands_fp->get()(1))-317.9111);
        myFile.printf("\n");

        myFile.printf("Fin Commands: (");
        myFile.print(fin_commands_fp->get()(0));
        myFile.print(",");
        myFile.print(fin_commands_fp->get()(1));
        myFile.print(",");
        myFile.print(fin_commands_fp->get()(2));
        myFile.print(",");
        myFile.print(fin_commands_fp->get()(3));
        myFile.print(")\n");

        myFile.printf("Motor Commands: (");
        myFile.print(thrust_commands_fp->get()(0));
        myFile.print(",");
        myFile.print(thrust_commands_fp->get()(1));
        myFile.print(")\n");
    }
    myFile.flush();
}

void SDCardControlTask::actuate(){

}