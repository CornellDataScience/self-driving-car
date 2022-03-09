delta_t=.1;
t_total=30;
t=[0:delta_t:t_total];

%Initialization of Arrays
roll_theta=zeros(t_total/delta_t+1,1);
roll_omega=zeros(t_total/delta_t+1,1);
roll_alpha=zeros(t_total/delta_t+1,1);
roll_error=zeros(length(roll_theta),1);
roll_p_correction=zeros(length(roll_theta),1);
roll_integral=zeros(length(roll_theta),1);
roll_i_correction=zeros(length(roll_theta),1);
roll_derivative=zeros(length(roll_theta),1);
roll_d_correction=zeros(length(roll_theta),1);

%Initial Conditions
roll_theta(1)=0;
roll_omega(1)=160;
roll_alpha(1)=0;
%Gains
Kp_roll=1;
Ki_roll=0;
Kd_roll=0.9;

%Calculation
for i = 2:length(roll_theta)
    %Calculation
    roll_error(i)=-roll_theta(i-1);
    roll_p_correction(i)= Kp_roll*roll_error(i);
    roll_integral(i)=roll_integral(i-1)+roll_error(i)*delta_t;
    roll_i_correction(i)=Ki_roll*roll_integral(i);
    roll_derivative(i)=(roll_error(i)-roll_error(i-1))/delta_t;
    roll_d_correction(i)=Kd_roll*roll_derivative(i);
    roll_alpha(i)=roll_i_correction(i)+roll_p_correction(i)+roll_d_correction(i);
    %Physics
    roll_theta(i)=roll_theta(i-1)+roll_omega(i-1)*delta_t;
    roll_omega(i)=roll_omega(i-1)+roll_alpha(i-1)*delta_t;
end

%Plotting
plot (t,roll_omega)

xlabel('Time (sec)')
ylabel('Roll Angle (degrees)')
