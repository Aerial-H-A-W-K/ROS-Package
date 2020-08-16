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

class KiteVisual():
	def __init__(self):
		rospy.loginfo("Initialising..")
		self.x_pub = rospy.Publisher('/kite/gimbal_joint1_position_controller/command', Float64, queue_size=1)
		self.tilt_pub = rospy.Publisher('/kite/briddle_x_joint_position_controller/command', Float64, queue_size=1)
		self.tether_pub = rospy.Publisher('/kite/tether_joint_position_controller/command', Float64, queue_size=1)
		self._x_angle_object = Float64()
		self._tilt_angle_object = Float64()
		self._tether_object = Float64()
		self.x_ang = 0
		self.tilt_ang = 0
		self.tether_len = 0
		self._sub = rospy.Subscriber('/kite/joint_states', JointState, self.callback)
		self._position_dict = {"gimbal_joint1":0, "briddle _x_joint":0, "tether_joint":0}
	
	def callback(self, msg):
		self._position_dict = dict(zip(msg.name, msg.position))
		rospy.logdebug(self._position_dict)
		
	def get_ready(self):
		x_ang = -0.5
		tilt_ang = 0.4
		tether_len = 5
		self._x_angle_object.data = x_ang
		self._tilt_angle_object.data = tilt_ang
		self._tether_object.data = tether_len
		rate = rospy.Rate(1)
		self.x_pub.publish(self._x_angle_object)
		self.tilt_pub.publish(self._tilt_angle_object)
		self.tether_pub.publish(self._tether_object)
		rospy.loginfo("Moving to position")
		rate.sleep()
		similar = self.check_similar(x_ang, tilt_ang, tether_len)
		
		while not similar and not ctrl_c:	
			rospy.loginfo("Moving to position")
			self.x_pub.publish(self._x_angle_object)
			self.tilt_pub.publish(self._tilt_angle_object)
			self.tether_pub.publish(self._tether_object)
			rate.sleep()
			similar = self.check_similar(x_ang, tilt_ang, tether_len)
			
		rospy.loginfo("Ready for input")
		
		while not ctrl_c:
			self.move_by_input()
			
	def check_similar(self, x_ang=0, tilt_ang=0, tether_len=0):
		position_dict = self.get_data()
		actual_x = position_dict["gimbal_joint1"]
		diff_x = abs(actual_x - x_ang)
		actual_tilt = position_dict["briddle_x_joint"]
		diff_tilt = abs(actual_tilt - tilt_ang)
		actual_len = position_dict["tether_joint"]
		diff_len = abs(actual_len - tether_len)
		rospy.loginfo("diff_x = "+str(diff_x)+ ", diff_tilt = "+str(diff_tilt) +", diff_len = "+str(diff_len))
		similar = diff_x <= 0.06
		if similar:
			similar = diff_tilt <= 0.02
			if similar:
				similar = diff_len <= 1
		return similar
		
	def get_data(self):
		return self._position_dict
		
	def move_by_input(self):
		
		my_dict = {}
		my_dict[(5, 45)] = 40
		my_dict[(5, 50)] = 35
		my_dict[(5, 55)] = 30
		my_dict[(5, 60)] = 25
		
		my_dict[(6, 45)] = 40
		my_dict[(6, 50)] = 35
		my_dict[(6, 55)] = 30
		my_dict[(6, 60)] = 25
		
		my_dict[(7, 45)] = 40
		my_dict[(7, 50)] = 35
		my_dict[(7, 55)] = 30
		my_dict[(7, 60)] = 25
		
		my_dict[(8, 45)] = 40
		my_dict[(8, 50)] = 35
		my_dict[(8, 55)] = 30
		my_dict[(8, 60)] = 25
		
		my_dict[(9, 45)] = 45
		my_dict[(9, 50)] = 40
		my_dict[(9, 55)] = 35
		my_dict[(9, 60)] = 30
		
		my_dict[(10, 45)] = 45
		my_dict[(10, 50)] = 40
		my_dict[(10, 55)] = 35
		my_dict[(10, 60)] = 30
		
		
		
		

		while True:
			windspeed = input("Please input windspeed from 5 to 10: ")
			desired_tether_angle = input("Please input desired tether angle in multiples of 5 between 45 to 60: ")
			calc_AOA = my_dict[windspeed,desired_tether_angle]
			rospy.loginfo("Calculated angle of attack of parafoil = "+ str(calc_AOA) + "degrees")
			position_dict = self.get_data()
			calc_AOA = calc_AOA * 0.0174533
			x_ang = position_dict["gimbal_joint1"]
			tether_len = position_dict["tether_joint"]
			initial_tilt_ang = calc_AOA - (1.5708 + x_ang)
			self._tilt_angle_object.data = initial_tilt_ang
			self.tilt_pub.publish(self._tilt_angle_object)
			rospy.loginfo("Pitching parafoil to calculated pitch angle")
			rate.sleep()
			similar = self.check_similar(x_ang, initial_tilt_ang, tether_len)
			while not similar and not ctrl_c:
				self.tilt_pub.publish(self._tilt_angle_object)
				rate.sleep()
				similar = self.check_similar(x_ang, initial_tilt_ang, tether_len)
			rospy.loginfo("Parafoil is now reacting to forces due to pitch angle")
			x_ang = (90-desired_tether_angle)*(-0.0174533)
			self._x_angle_object.data = x_ang
			similar = self.check_similar(x_ang, initial_tilt_ang, tether_len)
			while not similar and not ctrl_c:
				self.x_pub.publish(self._x_angle_object)
				self.tilt_pub.publish(self._tilt_angle_object)
				self.tether_pub.publish(self._tether_object)
				rate.sleep()
				similar = self.check_similar(x_ang, initial_tilt_ang, tether_len)	
			final_tilt_ang = ((90 - desired_tether_angle) * 0.0174533) - calc_AOA
			self._tilt_angle_object.data = final_tilt_ang
			tether_len = tether_len + 5
			self._tether_object.data = tether_len
			similar = self.check_similar(x_ang, final_tilt_ang, tether_len)
			while not similar and not ctrl_c:
				self.x_pub.publish(self._x_angle_object)
				self.tilt_pub.publish(self._tilt_angle_object)
				self.tether_pub.publish(self._tether_object)
				rate.sleep()
				similar = self.check_similar(x_ang, final_tilt_ang, tether_len)
			while tether_len < 20:
				tether_len = tether_len + 5
				self._tether_object.data = tether_len
				similar = self.check_similar(x_ang, final_tilt_ang, tether_len)
				while not similar and not ctrl_c:
					self.x_pub.publish(self._x_angle_object)
					self.tilt_pub.publish(self._tilt_angle_object)
					self.tether_pub.publish(self._tether_object)
					rate.sleep()
					similar = self.check_similar(x_ang, final_tilt_ang, tether_len)
			rospy.loginfo("Maximum tether length reached!")
			rospy.loginfo("Tilting parafoil to angle of maximum upward force")
			zero_AOA = final_tilt_ang + calc_AOA
			self._tilt_angle_object.data = zero_AOA
			similar = self.check_similar(x_ang, zero_AOA, tether_len)
			while not similar and not ctrl_c:
				self.x_pub.publish(self._x_angle_object)
				self.tilt_pub.publish(self._tilt_angle_object)
				self.tether_pub.publish(self._tether_object)
				rate.sleep()
				similar = self.check_similar(x_ang, zero_AOA, tether_len)
			rospy.loginfo("Moving system to vertical position")
			self._x_angle_object.data = 0
			self._tilt_angle_object.data = 0
			similar = self.check_similar(0, 0, tether_len)
			while not similar and not ctrl_c:
				self.x_pub.publish(self._x_angle_object)
				self.tilt_pub.publish(self._tilt_angle_object)
				rate.sleep()
				similar = self.check_similar(0, 0, tether_len)
			rospy.loginfo("Beginning reeling in of system")
			tether_len = tether_len - 15
			self._tether_object.data = tether_len
			similar = self.check_similar(0, 0, tether_len)
			while not similar and not ctrl_c:
				self.x_pub.publish(self._x_angle_object)
				self.tilt_pub.publish(self._tilt_angle_object)
				self.tether_pub.publish(self._tether_object)
				rate.sleep()
				similar = self.check_similar(0, 0, tether_len)
#			position_dict = {"gimbal_joint1":0.0, "briddle _x_joint":0.0, "tether_joint":5.0}
#			x_ang = position_dict["gimbal_joint1"]
#			tether_len = position_dict["tether_joint"]
#			self._x_angle_object.data = x_ang
#			initial_tilt_ang = calc_AOA - (1.5708 - x_ang)
#			self._tilt_angle_object.data = initial_tilt_ang
#			self.tilt_pub.publish(self._tilt_angle_object)
#			rospy.loginfo("Pitching parafoil to calculated pitch angle")
#			rate.sleep()
#			similar = self.check_similar(x_ang, initial_tilt_ang, tether_len)
#			while not similar and not ctrl_c:
#				self.tilt_pub.publish(self._tilt_angle_object)
#				rate.sleep()
#				similar = self.check_similar(x_ang, initial_tilt_ang, tether_len)
#			rospy.loginfo("Parafoil is now reacting to forces due to pitch angle")
#			
#			x_ang = (90-desired_tether_angle)*(-0.0174533)
#			self._x_angle_object.data = x_ang
#			similar = self.check_similar(x_ang, initial_tilt_ang, tether_len)
#			while not similar and not ctrl_c:
#				self.x_pub.publish(self._x_angle_object)
#				self.tilt_pub.publish(self._tilt_angle_object)
#				self.tether_pub.publish(self._tether_object)
#				rate.sleep()
#				similar = self.check_similar(x_ang, initial_tilt_ang, tether_len)	
#			final_tilt_ang = ((90 - desired_tether_angle) * 0.0174533) - calc_AOA
#			self._tilt_angle_object.data = final_tilt_ang
#			tether_len = tether_len + 5
#			self._tether_object.data = tether_len
#			similar = self.check_similar(x_ang, final_tilt_ang, tether_len)
#			while not similar and not ctrl_c:
#				self.x_pub.publish(self._x_angle_object)
#				self.tilt_pub.publish(self._tilt_angle_object)
#				self.tether_pub.publish(self._tether_object)
#				rate.sleep()
#				similar = self.check_similar(x_ang, final_tilt_ang, tether_len)	
				
		else:
			pass
				
		
		
if __name__ == '__main__':
	rospy.init_node('kite_loop', log_level=rospy.INFO)
	kite_object = KiteVisual()
	rate = rospy.Rate(1)
	ctrl_c = False
	def shutdownhook():
		global ctrl_c
		print ("Shutdown time")
		ctrl_c = True
	rospy.on_shutdown(shutdownhook)
	while not ctrl_c:
		kite_object.get_ready()
		
		
	
