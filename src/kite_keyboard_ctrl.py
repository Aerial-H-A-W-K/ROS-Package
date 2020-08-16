#!/usr/bin/env python 

import sys 
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
import sys, select, termios, tty 

  
msg = """ 
Reading from the keyboard and publishing movement! 

--------------------------- 

Adjust pitch: 
   i   ,

Adjust roll:
   j   l
   
Adjust yaw:
   u   o

Moving tether:
   m   .

anything else : stop 


CTRL-C to quit 

""" 


movementBindings={ 
                'i':(0.1,0,0,0),
                ',':(-0.1,0,0,0),
                'j':(0,0.1,0,0),
                'l':(0,-0.1,0,0),
                'u':(0,0,0.1,0),
                'o':(0,0,-0.1,0),
                'm':(0,0,0,5),
                '.':(0,0,0,-5)
              } 

  

def getKey(): 
        tty.setraw(sys.stdin.fileno()) 
        select.select([sys.stdin], [], [], 0) 
        key = sys.stdin.read(1) 
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings) 
        return key 
        
 

def val(x_ang, y_ang, z_ang, tether_len): 
        return "x_ang = "+ str(x_ang) + ", y_ang = " + str(y_ang) + ", z_ang = " + str(z_ang) + ", tether_len = " + str(tether_len) 

  
  
if __name__ == '__main__': 
    settings = termios.tcgetattr(sys.stdin) 
  
    if len(sys.argv) < 2: 
        print("usage: move_generic_model.py model_name") 

    else: 
        model_name = sys.argv[1] 
        print "Found Model Name" 
  
    x_pub = rospy.Publisher('/kite/briddle_x_joint_position_controller/command', Float64, queue_size=1)
    y_pub = rospy.Publisher('/kite/briddle_y_joint_position_controller/command', Float64, queue_size=1)
    z_pub = rospy.Publisher('/kite/briddle_z_joint_position_controller/command', Float64, queue_size=1)
    tether_pub = rospy.Publisher('/kite/tether_joint_position_controller/command', Float64, queue_size=1)

    x_angle_object = Float64()
    y_angle_object = Float64()
    z_angle_object = Float64()
    tether_object = Float64()
    
    x_ang = 0.0
    y_ang = 0.0
    z_ang = 0.0
    tether_len = 5

    rospy.init_node('keyboard_input') 
    
    rate = rospy.Rate(1)



    try:
        x_angle_object.data = x_ang
        y_angle_object.data = y_ang
        z_angle_object.data = z_ang
        tether_object.data = tether_len
        
        x_pub.publish(x_angle_object)
        y_pub.publish(y_angle_object)
        z_pub.publish(z_angle_object)
        tether_pub.publish(tether_object)
        print msg 
        print val(x_ang, y_ang, z_ang, tether_len)
        while(1): 
                key = getKey() 
                if key in movementBindings.keys(): 
                        x_ang = x_ang + movementBindings[key][0]
                        y_ang = y_ang + movementBindings[key][1]
                        z_ang = z_ang + movementBindings[key][2]
                        tether_len = tether_len + movementBindings[key][3]
                        print val(x_ang, y_ang, z_ang, tether_len)

                else: 
			pass

  

                x_angle_object.data = x_ang
                y_angle_object.data = y_ang
                z_angle_object.data = z_ang
                tether_object.data = tether_len
                
                x_pub.publish(x_angle_object)
                y_pub.publish(y_angle_object)
                z_pub.publish(z_angle_object)
                tether_pub.publish(tether_object)
                #rate.sleep(1)



    except Exception as e:
        print(e)

      

    finally: 
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings) 
