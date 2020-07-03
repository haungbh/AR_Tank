#!/usr/bin/env python
from __future__ import print_function

import roslib
roslib.load_manifest('final')
import rospy
import cv2
import sys
import os
from std_msgs.msg import String
from std_msgs.msg import UInt16
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from geometry_msgs.msg import Twist
import finder
import trace_marker

class image_converter:
	

	def __init__(self):
		self.image_pub = rospy.Publisher("image_topic_2",Image,queue_size=1)
		self.pub = rospy.Publisher('/RosAria/cmd_vel', Twist, queue_size = 1)
		self.pub_cannon_servo = rospy.Publisher('servo', UInt16, queue_size = 1)
		self.pub_cannon_relay = rospy.Publisher('relay', UInt16, queue_size = 1)
		
		self.relay_state = False

		self.bridge = CvBridge()
		#self.image_sub = rospy.Subscriber("camera/color/image_raw",Image,self.callback)
		self.image_sub = rospy.Subscriber("usb_cam/image_raw",Image,self.callback)

	def callback(self,data):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
		except CvBridgeError as e:
			print(e)

		(rows,cols,channels) = cv_image.shape
		#if cols > 60 and rows > 60 :
			#cv2.circle(cv_image, (50,50), 10, 255)
		"""cv_image = cv2.medianBlur(cv_image,5)
		gray_img = cv2.cvtColor(cv_image,cv2.COLOR_BGR2GRAY)o
		circles = cv2.HoughCircles(gray_img,cv2.HOUGH_GRADIENT,1,100,param1=50,param2=30,minRadius=50,maxRadius=100)

		circles = np.uint16(np.around(circles))

		for i in circles[0,:]:
			# draw the outer circle
			cv2.circle(cv_image,(i[0],i[1]),i[2],(0,255,0),2)
			# draw the center of the circle
			cv2.circle(cv_image,(i[0],i[1]),2,(0,0,255),3)"""
		
		speed = rospy.get_param("~speed", 0.5)
		turn = rospy.get_param("~turn", 0.5)
		th = 0
		flag = 0
		sp = 0

		
		ids, center = trace_marker.get_marker(cv_image)
		cv2.line(cv_image, (280, 0), (280, 480), (0, 0, 255), 2)
		cv2.line(cv_image, (360, 0), (360, 480), (0, 0, 255), 2)
		#cv2.circle(cv_image,(center_x,center_y),60,(0,255,0),2)
				
		if flag == 0 and center is not None:
			# target in sight

			# turn on accelerator
			if not self.relay_state:
				self.pub_cannon_relay.publish(1)
				self.relay_state = True

			# trace marker
			if center[0][0] < 300:
				th = 0.2
				print("turn left")
			elif center[0][0] > 340:
				th = -0.2
				print("turn right")
			else:
				th = 0
				flag = 1
				print("dont move")
		else:
			# search for target
			th = -0.4
			# turn off accelerator
			if self.relay_state:
				self.pub_cannon_relay.publish(0)
				self.relay_state = False


		if flag == 1:
			if center[0][1] < 220:
				sp = -0.5
			elif center[0][1] > 260:
				sp = 0.5
			else:
				# reach target
				sp = 0
				flag = 0
				# should only trigger once
				self.pub_cannon_servo.publish(80)
				
				
		
		twist = Twist()
		twist.linear.x = sp*speed
		twist.linear.y = 0*speed
		twist.linear.z = 0*speed
		twist.angular.x = 0
		twist.angular.y = 0
		twist.angular.z = th*turn

		self.pub.publish(twist)
		if center is not None:
			print(center[0][1])
		#cv2.imshow("./123.png", cv_image)
		cv2.waitKey(3)

		try:
			self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
		except CvBridgeError as e:
			print(e)
		
		
		#rospy.signal_shutdown("")
def start(data):
	ic = image_converter()
	

def main(args):
	
	rospy.init_node('image_converter', anonymous=True)
	#ic = image_converter()
	sub = rospy.Subscriber("chatter",String, start)
	#rate = rospy.Rate(50000)
	#rate.sleep()
	
	try:
		rospy.spin()
	except KeyboardInterrupt:
		print("Shutting down")
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main(sys.argv)
	
