#!/usr/bin/env python

import rospy
from std_msgs.msg import UInt16

import sys, select, termios, tty

def getKey():
	tty.setraw(sys.stdin.fileno())
	select.select([sys.stdin], [], [], 0)
	key = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key

if __name__=="__main__":
	settings = termios.tcgetattr(sys.stdin)

	servo_pub = rospy.Publisher('servo', UInt16, queue_size = 1)
	accel_pub = rospy.Publisher('relay', UInt16, queue_size = 1)

	rospy.init_node('cannon_controller')

	accel_on = False

	try:
		while not rospy.is_shutdown():
			key = getKey()
			if key == ' ':
				print("Fire!")
				servo_pub.publish(80)
			elif key == 'r':
				accel_on = not accel_on
				if accel_on:
					print("Relay on")
					accel_pub.publish(1)
				else:
					print("Relay off")
					accel_pub.publish(0)
			elif key == 'e':
				print("system down")
				break
				
	except Exception as e:
		print(e)

