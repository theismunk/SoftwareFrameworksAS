#!/usr/bin/env python
# This program publishes randomly-generated velocity
# messages for turtlesim.
import rospy
import numpy as np # For random numbers
global speed_var
global tmp_speed
speed_var= 1.0
tmp_speed=speed_var
rospy.set_param('speed_of_turtle', speed_var)
 
 
from std_msgs.msg import String
from geometry_msgs.msg import Twist #For geometry_msgs/Twist
from hello_ros.msg import turtle #For geometry_msgs/Twist
 
#Create callback. This is what happens when a new message is received
def sub_cal(msg):
    rospy.loginfo("name= %s, speed= %f", msg.name, msg.speed)
    global speed_var
    speed_var = msg.speed
    rospy.set_param('speed_of_turtle',speed_var)
 
#Initialize publisher
p = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=1000)
#Initialise subscriber
rospy.Subscriber('turtle1/turtle_speed', turtle, sub_cal, queue_size=1000)
 
 
 
# Initialize node
rospy.init_node('publish_variable_velocity')
r = rospy.Rate(2) # Set Frequency
 
#loop until someone shutds us down..
while not rospy.is_shutdown():
 
    #Initiate Message with zero values
    t=Twist()
    #Fill in message
    speed_of_turtle = rospy.get_param('speed_of_turtle')
    if speed_of_turtle is not tmp_speed:
        speed_var=speed_of_turtle
        tmp_speed=speed_of_turtle
 
    t.angular.z = (2*np.random.rand()-1)*speed_var
    t.linear.x = (np.random.rand())*speed_var
 
    #ROS INFO of the commands
    #rospy.loginfo("Ang.z is%s" % t.angular.z)
    #rospy.loginfo("Lin.x is%s" % t.linear.x)
 
    #publish the message
    p.publish(t)
    r.sleep()