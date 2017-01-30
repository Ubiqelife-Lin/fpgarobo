#!/usr/bin/python
# -*- coding: utf-8 -*-
# license removed for brevity
import rospy
from bridge import Xillybus
from fpgarobo.msg import FpgaroboMsg

class Fpgarobo(object):
	def __init__(self):
		self.if_32 = Xillybus(32)
		self.if_32.open_dev_write()
		self.if_32.open_dev_read()
		self.input_para_in_right = 0
		self.input_dir_in_right = 0
		self.input_para_in_left = 0
		self.input_dir_in_left = 0
		self.output_out_data = None
		self.cur_data = 0

		self.msg = FpgaroboMsg()
		self.pub = rospy.Publisher('fpgarobo_output', FpgaroboMsg, queue_size=100)
	def pack_32(self):
		data = 0
		data = data + (self.input_para_in_right << 0)
		data = data + (self.input_dir_in_right << 15)
		data = data + (self.input_para_in_left << 16)
		data = data + (self.input_dir_in_left << 31)
		data = self.if_32.adjust(data, mode = 32)
		return data
	
	def callback(self, data):
		self.input_para_in_right = data.input_para_in_right
		self.input_dir_in_right = data.input_dir_in_right
		self.input_para_in_left = data.input_para_in_left
		self.input_dir_in_left = data.input_dir_in_left
		self.output_out_data = 0
		
		self.if_32.write(self.pack_32())
		# please describe message data to publish
		# self.msg.output_out_data = self.if_32.read(1)
		sensor_data = self.if_32.read(4)
		# self.fo.write(self.msg.output_out_data)
		if self.cur_data != sensor_data and self.cur_data != 1:
			print "sensor value is %s"%sensor_data
		self.cur_data = sensor_data
		# self.pub.publish(self.msg)

	def fpgarobo(self):
		print "start fpgarobo_node"
		rospy.init_node('fpgarobo_node', anonymous=True)
		rospy.Subscriber('fpgarobo_input', FpgaroboMsg, self.callback)
		rospy.spin()

if __name__ == '__main__':
	fpgarobo = Fpgarobo()
	fpgarobo.fpgarobo()