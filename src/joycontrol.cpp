#include "ros/ros.h"
#include "geometry_msgs/Twist.h"
#include <sensor_msgs/Joy.h>
#include "std_msgs/UInt16.h"
 
ros::Publisher pioneer_vel;
ros::Publisher cannon_servo;
ros::Publisher cannon_relay;

int preAState = 0;
int preBState = 0;
int relayState = 0;
 
void joyCallback(const sensor_msgs::Joy::ConstPtr& joy)
{
	ROS_INFO("I heard: linear_:[%f]   angular_[%d]", joy->axes[1], joy->axes[0]);
  	geometry_msgs::Twist twist;
	twist.linear.x = joy->axes[1] > 0 ? (joy->axes[1] > 0.5 ? 0.5 : joy->axes[1]) : (joy->axes[1] < -0.5 ? -0.5 : joy->axes[1]) ;
	twist.linear.y = 0;
	twist.angular.z = joy->axes[0] > 0 ? (joy->axes[0] > 0.5 ? 0.5 : joy->axes[0]) : (joy->axes[0] < -0.5 ? -0.5 : joy->axes[0]);
 	pioneer_vel.publish(twist);

        // cannon control
	if(joy->buttons[0] == 1 && preAState < 1){
		cannon_servo.publish(80); 
        }
        if(joy->buttons[1] == 1 && preBState < 1){
                if(relayState == 0){
                        cannon_relay.publish(1);
                        relayState = 1;
                }else{
                        cannon_relay.publish(0);
                        relayState = 0;
                }
        }
        preAState = joy->buttons[0];
        preBState = joy->buttons[1];

}
 
int main(int argc, char **argv)
{
 
        // initialize ros
        ros::init(argc, argv, "Joystick_controller");
	ros::NodeHandle n;
 
        // create publisher
 
        pioneer_vel = n.advertise<geometry_msgs::Twist>("/RosAria/cmd_vel", 1000);

        cannon_servo = n.advertise<std_msgs::UInt16>("servo", 1);
        cannon_relay = n.advertise<std_msgs::UInt16>("relay", 1);
 
        ros::Subscriber joy_command = n.subscribe<sensor_msgs::Joy>("joy", 10, joyCallback);
 
        // our loop will publish at 10Hz
        ros::Rate loop_rate(5);
 
	ros::spin();
}
