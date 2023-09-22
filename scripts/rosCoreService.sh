#!/bin/bash
source /home/protomates2/.bashrc
source /opt/ros/noetic/setup.bash
source /home/protomates2/catkin_ws/devel/setup.bash
roslaunch mavros apm.launch fcu_url:=/dev/ttyS1:115200 &/bin/sleep 120;
rosrun protomates subscribe.py & /bin/python3 /home/protomates2/catkin_ws/src/protomates/scripts/push.py
