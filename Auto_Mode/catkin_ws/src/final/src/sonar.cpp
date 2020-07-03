#include "ros/ros.h"
#include "sensor_msgs/PointCloud.h"

  
void chatterCallback(const sensor_msgs::PointCloud& msg)
{

   ROS_INFO("Sonar X: [%f]", msg.points[0].x);
   ROS_INFO("Sonar Y: [%f]", msg.points[0].y);
   ROS_INFO("hello");
}
  
int main(int argc, char **argv)
{
   ros::init(argc, argv, "sonar_listener");
 
   ros::NodeHandle n;
  
   ros::Subscriber sub = n.subscribe("RosAria/sonar", 1000, chatterCallback);
   

  
   ros::spin();
   
   return 0;
}
