#!/usr/bin/env python 
import rospy
import tf
import math
 
if __name__ == '__main__':
    rospy.init_node('moving_tf_broadcaster')
    br = tf.TransformBroadcaster()
    rate = rospy.Rate(10.0)
    rotation = (0, 0, 0, 1)
    translation = (2.0, 0.0, 0.0)
    while not rospy.is_shutdown():
        t = rospy.Time.now().to_sec()
        translation = (2.0 * math.cos(t), 2.0 * math.sin(t), 0)
        br.sendTransform(translation,
                         rotation,
                         rospy.Time.now(),
                         "carrot1",
                         "turtle1")
        rate.sleep()