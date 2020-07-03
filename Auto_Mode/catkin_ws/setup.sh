#!/bin/bash
echo "final project"


sudo chmod 777 /dev/ttyUSB0
sudo chmod 777 /dev/ttyUSB1
sudo chmod 777 /dev/ttyACM0
sudo chmod 777 /dev/ttyACM1

gnome-terminal -x bash -c "roscore;exec bash"

sleep 3s

gnome-terminal -x bash -c "rosrun rosaria RosAria"
sleep 1s
gnome-terminal -x bash -c "rosrun urg_node urg_node"
sleep 1s
gnome-terminal -x bash -c "roslaunch lzrobot map_server.launch"
sleep 1s
gnome-terminal -x bash -c "roslaunch lzrobot amcl_pioneer.launch"
sleep 1s
gnome-terminal -x bash -c "roslaunch usb_cam usb_cam-test.launch"
sleep 1s

gnome-terminal -x bash -c "rviz"
sleep 3s

gnome-terminal -x bash -c "rosrun teleop_twist_keyboard teleop_twist_keyboard.py cmd_vel:=/RosAria/cmd_vel"
