#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
 
def hello_ros():
    rospy.init_node('hello_ros', anonymous=True)
    rate = rospy.Rate(5) # 10hz
    
    while not rospy.is_shutdown():
        hello_str = "hello ros!!! %s" % rospy.get_time()
        rospy.loginfo(hello_str)
 
if __name__ == '__main__':
    try:
        hello_ros()
    except rospy.ROSInterruptException:
        pass