#!/bin/bash
echo "final project"

gnome-terminal -x bash -c "roslaunch lzrobot move_base.launch"
sleep 3s

gnome-terminal -x bash -c "rosrun lzrobot simple_navigation_goals"
sleep 5s

gnome-terminal -x bash -c "rosrun final image.py"
