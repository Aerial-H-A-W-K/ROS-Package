#! /usr/bin/env python

import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
import sys

"""
Topics To Write on:
type: std_msgs/Float64
/kite/briddle_x_joint_position_controller/command
/kite/gimbal_joint1_position_controller/command
/kite/tether_joint_position_controller/command
"""

class KiteMover():
	def __init__(self):
		rospy.loginfo("Initialising..")
		self.x_pub = rospy.Publisher('/kite/gimbal_joint1_position_controller/command', Float64, queue_size=1)
		self.tilt_pub = rospy.Publisher('/kite/briddle_x_joint_position_controller/command', Float64, queue_size=1)
		self.tether_pub = rospy.Publisher('/kite/tether_joint_position_controller/command', Float64, queue_size=1)
		rospy.loginfo("Line 23")
		self._x_angle_object = Float64()
		self._y_angle_object = Float64()
		self._z_angle_object = Float64()
		self._tether_object = Float64()
		rospy.loginfo("Line 28")
		self.x_ang = 0
		self.y_ang = 0
		self.z_ang = 0
		self.tether_len = 10
		rospy.loginfo("Line 33")
		self._sub = rospy.Subscriber('/kite/joint_states', JointState, self.callback)
		rospy.loginfo("Line 35")
		self._position_dict = {"gimbal_joint1":0, "gimbal_joint2":0, "gimbal_joint3":0, "tether_joint":0}
		rospy.loginfo("Line 37")
		
	def callback(self, msg):
		self._position_dict = dict(zip(msg.name, msg.position))
		rospy.logdebug(self._position_dict)
		
		
	def move_loop(self):
		self.x_ang = -0.5
		self.y_ang = -0.5
		self.z_ang = 0.2
		self.tether_len = 10
		self._x_angle_object.data = self.x_ang
		self._y_angle_object.data = self.y_ang
		self._z_angle_object.data = self.z_ang
		self._tether_object.data = self.tether_len
		similar = self.check_similar(self.x_ang, self.y_ang, self.z_ang, self.tether_len)
		rate = rospy.Rate(1)
		self.x_pub.publish(self._x_angle_object)
		self.y_pub.publish(self._y_angle_object)
		self.z_pub.publish(self._z_angle_object)
		self.tether_pub.publish(self._tether_object)
		rospy.loginfo("Moving to position")
		while not similar:
			similar = self.check_similar(self.x_ang, self.y_ang, self.z_ang, self.tether_len)
		rospy.loginfo("Reached position")
		
		self.x_ang = -0.5
		self.y_ang = 0.5
		self.z_ang = -0.2
		self.tether_len = 15
		self._x_angle_object.data = self.x_ang
		self._y_angle_object.data = self.y_ang
		self._z_angle_object.data = self.z_ang
		self._tether_object.data = self.tether_len
		similar = self.check_similar(self.x_ang, self.y_ang, self.z_ang, self.tether_len)
		rate = rospy.Rate(1)
		self.x_pub.publish(self._x_angle_object)
		self.y_pub.publish(self._y_angle_object)
		self.z_pub.publish(self._z_angle_object)
		self.tether_pub.publish(self._tether_object)
		rospy.loginfo("Moving to position")

		while not similar:
			#rate.sleep()
			similar = self.check_similar(self.x_ang, self.y_ang, self.z_ang, self.tether_len)
		rospy.loginfo("Reached position")
		
		self.x_ang = -0.8
		self.y_ang = 0.5
		self.z_ang = -0.2
		self.tether_len = 20
		self._x_angle_object.data = self.x_ang
		self._y_angle_object.data = self.y_ang
		self._z_angle_object.data = self.z_ang
		self._tether_object.data = self.tether_len
		similar = self.check_similar(self.x_ang, self.y_ang, self.z_ang, self.tether_len)
		rate = rospy.Rate(10)
		self.x_pub.publish(self._x_angle_object)
		self.y_pub.publish(self._y_angle_object)
		self.z_pub.publish(self._z_angle_object)
		self.tether_pub.publish(self._tether_object)
		rospy.loginfo("Moving to position")

		while not similar:
			#rate.sleep()
			similar = self.check_similar(self.x_ang, self.y_ang, self.z_ang, self.tether_len)
		rospy.loginfo("Reached position")
		
		self.x_ang = -0.8
		self.y_ang = -0.5
		self.z_ang = 0.2
		self.tether_len = 25
		self._x_angle_object.data = self.x_ang
		self._y_angle_object.data = self.y_ang
		self._z_angle_object.data = self.z_ang
		self._tether_object.data = self.tether_len
		similar = self.check_similar(self.x_ang, self.y_ang, self.z_ang, self.tether_len)
		rate = rospy.Rate(100)
		self.x_pub.publish(self._x_angle_object)
		self.y_pub.publish(self._y_angle_object)
		self.z_pub.publish(self._z_angle_object)
		self.tether_pub.publish(self._tether_object)
		rospy.loginfo("Moving to position")

		while not similar:
			#rate.sleep()
			similar = self.check_similar(self.x_ang, self.y_ang, self.z_ang, self.tether_len)
		rospy.loginfo("Reached position")

			
			
	def get_data(self):
		return self._position_dict
		
		

	def check_similar(self, x_ang=0, y_ang=0, z_ang=0, tether_len=0):
		position_dict = self.get_data()
		actual_x = position_dict["gimbal_joint1"]
		diff_x = abs(actual_x - x_ang)
		actual_y = position_dict["gimbal_joint2"]
		diff_y = abs(actual_y - y_ang)
		actual_z = position_dict["gimbal_joint3"]
		diff_z = abs(actual_z - z_ang)
		actual_len = position_dict["tether_joint"]
		diff_len = abs(actual_len - tether_len)
		rospy.loginfo("diff_x = "+str(diff_x)+ ", diff_y = "+str(diff_y) +", diff_z = "+str(diff_z) +", diff_len = "+str(diff_len))
		similar = diff_x <= 0.02
		if similar:
			similar = diff_y <= 0.02
			if similar:
				similar = diff_z <= 0.02
				if similar:
					similar = diff_len <= 1
		return similar
		
	def move_by_key(self):
		s = raw_input(':- ')
		position_dict = self.get_data()
		actual_x = position_dict["gimbal_joint1"]
		actual_y = position_dict["gimbal_joint2"]
		actual_z = position_dict["gimbal_joint3"]
		actual_len = position_dict["tether_joint"]
		if s[0] == "w":
			tether_len = actual_len + 5
			self._x_angle_object.data = actual_x
			self._y_angle_object.data = actual_y
			self._z_angle_object.data = actual_z
			self._tether_object.data = tether_len
			self.tether_pub.publish(self._tether_object)
			rospy.loginfo("Moving to position")
			similar = self.check_similar(actual_x, actual_y, actual_z, tether_len)
			
			while not similar:	
				rospy.loginfo("Moving to position")
				self.x_pub.publish(self._x_angle_object)
				self.y_pub.publish(self._y_angle_object)
				self.z_pub.publish(self._z_angle_object)
				self.tether_pub.publish(self._tether_object)
				rate.sleep()
				similar = self.check_similar(actual_x, actual_y, actual_z, tether_len)
				
		elif s[0] == "s":
			tether_len = actual_len - 5
			self._x_angle_object.data = actual_x
			self._y_angle_object.data = actual_y
			self._z_angle_object.data = actual_z
			self._tether_object.data = tether_len
			self.tether_pub.publish(self._tether_object)
			rospy.loginfo("Moving to position")
			similar = self.check_similar(actual_x, actual_y, actual_z, tether_len)
			
			while not similar:	
				rospy.loginfo("Moving to position")
				self.x_pub.publish(self._x_angle_object)
				self.y_pub.publish(self._y_angle_object)
				self.z_pub.publish(self._z_angle_object)
				self.tether_pub.publish(self._tether_object)
				rate.sleep()
				similar = self.check_similar(actual_x, actual_y, actual_z, tether_len)
		
		elif s[0] == "a":
			y_ang = actual_y - 0.1
			self._x_angle_object.data = actual_x
			self._y_angle_object.data = y_ang
			self._z_angle_object.data = actual_z
			self._tether_object.data = actual_len
			self.tether_pub.publish(self._y_angle_object)
			rospy.loginfo("Moving to position")
			similar = self.check_similar(actual_x, y_ang, actual_z, actual_len)
			
			while not similar:	
				rospy.loginfo("Moving to position")
				self.x_pub.publish(self._x_angle_object)
				self.y_pub.publish(self._y_angle_object)
				self.z_pub.publish(self._z_angle_object)
				self.tether_pub.publish(self._tether_object)
				rate.sleep()
				similar = self.check_similar(actual_x, y_ang, actual_z, actual_len)
				
		elif s[0] == "d":
			y_ang = actual_y + 0.1
			self._x_angle_object.data = actual_x
			self._y_angle_object.data = y_ang
			self._z_angle_object.data = actual_z
			self._tether_object.data = actual_len
			self.tether_pub.publish(self._y_angle_object)
			rospy.loginfo("Moving to position")
			similar = self.check_similar(actual_x, y_ang, actual_z, actual_len)
			
			while not similar:	
				rospy.loginfo("Moving to position")
				self.x_pub.publish(self._x_angle_object)
				self.y_pub.publish(self._y_angle_object)
				self.z_pub.publish(self._z_angle_object)
				self.tether_pub.publish(self._tether_object)
				rate.sleep()
				similar = self.check_similar(actual_x, y_ang, actual_z, actual_len)
				
		elif s[0] == "q":
			z_ang = actual_z - 0.1
			self._x_angle_object.data = actual_x
			self._y_angle_object.data = actual_y
			self._z_angle_object.data = z_ang
			self._tether_object.data = actual_len
			self.tether_pub.publish(self._z_angle_object)
			rospy.loginfo("Moving to position")
			similar = self.check_similar(actual_x, actual_y, z_ang, actual_len)
			
			while not similar:	
				rospy.loginfo("Moving to position")
				self.x_pub.publish(self._x_angle_object)
				self.y_pub.publish(self._y_angle_object)
				self.z_pub.publish(self._z_angle_object)
				self.tether_pub.publish(self._tether_object)
				rate.sleep()
				similar = self.check_similar(actual_x, actual_y, z_ang, actual_len)
				
		elif s[0] == "e":
			z_ang = actual_z + 0.1
			self._x_angle_object.data = actual_x
			self._y_angle_object.data = actual_y
			self._z_angle_object.data = z_ang
			self._tether_object.data = actual_len
			self.tether_pub.publish(self._z_angle_object)
			rospy.loginfo("Moving to position")
			similar = self.check_similar(actual_x, actual_y, z_ang, actual_len)
			
			while not similar:	
				rospy.loginfo("Moving to position")
				self.x_pub.publish(self._x_angle_object)
				self.y_pub.publish(self._y_angle_object)
				self.z_pub.publish(self._z_angle_object)
				self.tether_pub.publish(self._tether_object)
				rate.sleep()
				similar = self.check_similar(actual_x, actual_y, z_ang, actual_len)
		
		else:
			pass
		rospy.loginfo("Reach. Ready for next input")
				
	def get_ready(self):
		x_ang = 0
		y_ang = 0
		z_ang = 0
		tether_len = 10
		self._x_angle_object.data = x_ang
		self._y_angle_object.data = y_ang
		self._z_angle_object.data = z_ang
		self._tether_object.data = tether_len
		similar = self.check_similar(x_ang, y_ang, z_ang, tether_len)
		rate = rospy.Rate(1)
		self.x_pub.publish(self._x_angle_object)
		self.y_pub.publish(self._y_angle_object)
		self.z_pub.publish(self._z_angle_object)
		self.tether_pub.publish(self._tether_object)
		rospy.loginfo("Moving to position")
		rate.sleep()
		
		while not similar and not ctrl_c:	
			rospy.loginfo("Moving to position")
			self.x_pub.publish(self._x_angle_object)
			self.y_pub.publish(self._y_angle_object)
			self.z_pub.publish(self._z_angle_object)
			self.tether_pub.publish(self._tether_object)
			rate.sleep()
			similar = self.check_similar(x_ang, y_ang, z_ang, tether_len)
			
		rospy.loginfo("Ready for input")
		
		while not ctrl_c:
			self.move_by_key()

if __name__ == '__main__':
	rospy.init_node('kite_loop', log_level=rospy.INFO)
	kite_object = KiteMover()
	rate = rospy.Rate(1)
	ctrl_c = False
	def shutdownhook():
		global ctrl_c
		print ("Shutdown time")
		ctrl_c = True
	rospy.on_shutdown(shutdownhook)
	while not ctrl_c:
		kite_object.get_ready()
