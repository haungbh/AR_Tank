#if (ARDUINO >= 100)
 #include <Arduino.h>
#else
 #include <WProgram.h>
#endif

#include <Servo.h> 
#include <ros.h>
#include <std_msgs/UInt16.h>

// ROS
ros::NodeHandle nh;

// Servo motor
Servo servo;
int servoPin = 9;

// Relay
int relayPin = 8;

// Callbacks
void servo_cb(const std_msgs::UInt16& cmd_msg){
  // range: 0~180 degree
  servo.write(cmd_msg.data);
  delay(1000);
  servo.write(130);
  
}

void relay_cb(const std_msgs::UInt16& cmd_msg){
  // range: 0 or 1
  int state = cmd_msg.data;
  if(state == 0){
    digitalWrite(relayPin, LOW);
  }else{
    digitalWrite(relayPin, HIGH);
  }
}

// Subscribers
ros::Subscriber<std_msgs::UInt16> servo_sub("servo", servo_cb);
ros::Subscriber<std_msgs::UInt16> accel_sub("relay", relay_cb);

void setup(){
  // ROS
  nh.initNode();
  nh.subscribe(servo_sub);
  nh.subscribe(accel_sub);

  // servo
  servo.attach(servoPin);
  servo.write(120); //initial angle

  // relay
  pinMode(relayPin, OUTPUT);
  
}

void loop(){
  nh.spinOnce();
  delay(1);
}
