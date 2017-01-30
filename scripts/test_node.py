#!/usr/bin/python
# -*- coding: utf-8 -*-
# license removed for brevity
import rospy

from fpgarobo.msg import FpgaroboMsg

def fpgarobo_pub():
	print "start test_node"
	rospy.init_node('test_node', anonymous=True)
	pub = rospy.Publisher('fpgarobo_input', FpgaroboMsg, queue_size=100)

	r = rospy.Rate(10)
	msg = FpgaroboMsg()
	msg.input_para_in_right = 15000
	msg.input_dir_in_right = 1
	msg.input_para_in_left = 15000
	msg.input_dir_in_left = 1

	while not rospy.is_shutdown():
		pub.publish(msg)
		r.sleep()

def callback(data):
	# please desicribe your code
	pass

def fpgarobo_sub(self):
	rospy.init_node('fpgarobo_sub', anonymous=True)
	rospy.Subscriber('fpgarobo_output', FpgaroboMsg, callback)
	rospy.spin()

if __name__ == '__main__':
	fpgarobo_pub()