#!/usr/bin/env python
import rospy
import numpy as np

# rostopic pub /arm_controller/command trajectory_msgs/JointTrajectory '{joint_names: 
# ["hip", "shoulder", "elbow"], points: [{positions: [0.1, -0.5, 0.5], time_from_start:[1.0,0.0]}]}'

from std_msgs.msg import String
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

def talker():
  pub = rospy.Publisher('/arm_controller/command', JointTrajectory, queue_size=10)
  rospy.init_node('robot_pubpos', anonymous=True)
  rate = rospy.Rate(0.2) # 1 hz

  # loop while active
  while not rospy.is_shutdown():
    # create msg and point object
    msg=JointTrajectory()
    point=JointTrajectoryPoint()


    point.positions = [np.random.rand()*2-1, np.random.rand()*2-1, np.random.rand()*2-1]
    point.time_from_start = rospy.Duration(2)
    msg.joint_names=["hip","shoulder","elbow"]
    msg.points.append(point)

    pub.publish(msg)
    rate.sleep()

if __name__ == '__main__':
  try:
    talker()
  except rospy.ROSInterruptException:
    pass