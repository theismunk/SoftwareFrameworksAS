#!/usr/bin/env python  
import rospy
 
import tf
import turtlesim.msg
 
def handle_turtle_pose (msg, turtlename):
    br = tf.TransformBroadcaster()
    # send out the pose of the turtle in the form of a transform
    br.sendTransform((msg.x, msg.y, 0),
                     tf.transformations.quaternion_from_euler(0 , 0, msg.theta),
                     rospy.Time.now(),
                     turtlename,
                     "world")
 
if __name__ == '__main__':
    rospy.init_node( 'turtle_tf_broadcaster2' )
    turtlename = rospy.get_param('~turtle', default='turtle2')
    # subscribe to the pose of the turtle
    rospy.Subscriber( '/%s/pose' %  turtlename,
                     turtlesim.msg.Pose,
                     handle_turtle_pose,
                     turtlename)
    rospy.spin()