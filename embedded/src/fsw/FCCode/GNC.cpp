#include "GNC.hpp"

#include <lin.hpp>
#include <gnc/utilities.hpp>

GNC::GNC(StateFieldRegistry &registry, 
    unsigned int offset)
    : TimedControlTask<void>(registry, "gnc", offset),
    flap_commands_f("gnc.flap_cmds")
    {
        add_internal_field(flap_commands_f);
        mission_mode_fp = find_internal_field<unsigned char>("ls.mode", __FILE__, __LINE__);
        omega_vec_fp = find_internal_field<lin::Vector3f>("imu.gyr_vec", __FILE__, __LINE__);
        euler_vec_fp = find_internal_field<lin::Vector3f>("imu.euler_vec", __FILE__, __LINE__);
        quat_fp = find_internal_field<lin::Vector4d>("imu.quat", __FILE__, __LINE__);

        // default all flaps to no actuation
        flap_commands_f.set({
            0.0,
            0.0,
            0.0,
            0.0,
        });

        // testing
        lin::Vector4d frame_a_to_b{0,0,1,0}; //idk?
        lin::Vector3d v_in_a{0,1,0}; 
        lin::Vector3d v_in_b{0,1,0};


        gnc::utl::rotate_frame(frame_a_to_b, v_in_a, v_in_b);
        // b should now be mutated?

    }

void GNC::execute(){

    mission_mode_t mode = static_cast<mission_mode_t>(mission_mode_fp->get());

    switch(mode) {
        case mission_mode_t::warmup:
            // dispatch_warmup();
            break;
        case mission_mode_t::initialization:
            // dispatch_initialization();
            break;
        case mission_mode_t::standby:
            dispatch_detumble(); //detumble to prep fins into right orientation
            break;
        case mission_mode_t::detumble:
            dispatch_detumble();
            break;
        case mission_mode_t::bellyflop:
            dispatch_bellyflop();
            break;
        case mission_mode_t::landed:
            // dispatch_landed();
            break;
        default:
            printf(debug_severity::error, "Master state not defined: %d\n", static_cast<unsigned int>(mode));
            // mission_mode_fp->set(static_cast<unsigned char>(mission_mode_t::landed));
            break;
    }

}

void GNC::dispatch_sweep(){
    lin::Vector4f flap_commands = flap_commands_f.get();

    // the block below is dummy code that cycles the servos back and forth
    float speed = 0.5;
    if(flap_commands(0) > 90)
        inc_dir = -speed;
    if(flap_commands(0) <= 0)
        inc_dir = speed;
    for(unsigned int i = 0; i < SERVO::num_flaps; i++){
        flap_commands(i) += inc_dir;
    }

    flap_commands_f.set(flap_commands);
}

// not a real control law, just cool feedback
void GNC::omega_response(){
    lin::Vector3f omega = omega_vec_fp->get();
    float omega_norm = lin::norm(omega);
    if(omega_norm < 100.0)
        omega_norm = omega_norm*20;
    lin::Vector3f omega_scaled = (omega / omega_norm)*45.0 + 45.0*lin::ones<lin::Vector3f>();
    flap_commands_f.set({
        omega_scaled(0),
        omega_scaled(1),
        omega_scaled(2),
        omega_scaled(0),
    });
}

void GNC::euler_response(){
    lin::Vector3f euler = euler_vec_fp->get();

    lin::Vector3f euler_scaled = (euler / 100.0)*45.0 + 45.0*lin::ones<lin::Vector3f>();
    flap_commands_f.set({
        euler_scaled(0),
        euler_scaled(1),
        euler_scaled(2),
        euler_scaled(0),
    });    
}

void GNC::dispatch_detumble(){

    // everything 0 degrees of actuation
    flap_commands_f.set({
        0.0,
        0.0,
        0.0,
        0.0
    });
}
void GNC::dispatch_bellyflop(){

    // 1. READ SENSORS
    // 2. RUN PID LOOP
    // 3. ???
    // 4. PROFIT???

    // dispatch_sweep();
    // omega_response();
    euler_response();

}