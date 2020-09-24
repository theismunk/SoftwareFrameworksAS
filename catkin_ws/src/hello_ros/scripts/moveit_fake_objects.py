#!/usr/bin/env python
import roslib
roslib.load_manifest('hello_ros')
 
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import shape_msgs.msg as shape_msgs

# new 
import gazebo_msgs.msg

from std_msgs.msg import String

def GetObsPose():
  #Initialize publisher
  # 'wait_for_message' only asks once
  msg = rospy.wait_for_message('gazebo/model_states', gazebo_msgs.msg.ModelStates)

  hydrant_xyz = []
  check_str = "fire_hydrant"

  for i in range(len(msg.pose)):
    if msg.name[i][0:12] == check_str:
      hydrant_xyz.append(msg.pose[i].position.x)
      hydrant_xyz.append(msg.pose[i].position.y)
      hydrant_xyz.append(msg.pose[i].position.z)

  return hydrant_xyz


def move_group_python_interface_tutorial():
  ## BEGIN_TUTORIAL
  ## First initialize moveit_commander and rospy.
  print "============ Starting tutorial setup"
  moveit_commander.roscpp_initialize(sys.argv)
  rospy.init_node('move_group_python_interface_tutorial',
                  anonymous=True)
 
  ## Instantiate a RobotCommander object.  This object is an interface to
  ## the robot as a whole.
  robot = moveit_commander.RobotCommander()
 
  ## Instantiate a PlanningSceneInterface object.  This object is an interface
  ## to the world surrounding the robot.
  scene = moveit_commander.PlanningSceneInterface()
 
  ## Instantiate a MoveGroupCommander object.  This object is an interface
  ## to one group of joints.  In this case the group is the joints in the left
  ## arm.  This interface can be used to plan and execute motions on the left
  ## arm.
  group = moveit_commander.MoveGroupCommander("arm")
 
 
  ## We create this DisplayTrajectory publisher which is used below to publish
  ## trajectories for RVIZ to visualize.
  display_trajectory_publisher = rospy.Publisher(
                                      '/move_group/display_planned_path',
                                      moveit_msgs.msg.DisplayTrajectory)
 
  ## Wait for RVIZ to initialize. This sleep is ONLY to allow Rviz to come up.
  print "============ Waiting for RVIZ..."
  rospy.sleep(2)
  print "============ Starting tutorial "
 
  ## Getting Basic Information
  ## ^^^^^^^^^^^^^^^^^^^^^^^^^
  ##
  ## We can get the name of the reference frame for this robot
  print "============ Reference frame: %s" % group.get_planning_frame()
 
  ## We can also print the name of the end-effector link for this group
  print "============ Reference frame: %s" % group.get_end_effector_link()
 
  ## We can get a list of all the groups in the robot
  print "============ Robot Groups:"
  print robot.get_group_names()
 
  ## Sometimes for debugging it is useful to print the entire state of the
  ## robot.
  print "============ Printing robot state"
  print robot.get_current_state()
  print "============"
 
  scene = moveit_commander.PlanningSceneInterface()
  robot = moveit_commander.RobotCommander()
 
  rospy.sleep(2)
  '''
  scene.remove_world_object('groundplane')
  scene.remove_world_object('table')
  '''

  hydrant_xyz = GetObsPose()

  print "x pose 1: %f" % hydrant_xyz[0]
  print "y pose 1: %f" % hydrant_xyz[1]
  print "z pose 1: %f" % hydrant_xyz[2]
  print "x pose 2: %f" % hydrant_xyz[4]
  print "y pose 2: %f" % hydrant_xyz[4]
  print "z pose 2: %f" % hydrant_xyz[5]

  p = geometry_msgs.msg.PoseStamped()
  p.header.frame_id = robot.get_planning_frame()
  p.pose.position.x = hydrant_xyz[0]
  p.pose.position.y = hydrant_xyz[1]
  p.pose.position.z = hydrant_xyz[2] + 0.7
  scene.add_box("table", p, (0.5, 0.5, 1.4))
  p.pose.position.x = hydrant_xyz[3]
  p.pose.position.y = hydrant_xyz[4]
  p.pose.position.z = hydrant_xyz[5] + 0.7
  scene.add_box("table2", p, (0.5, 0.5, 1.4))
  p.pose.position.x = 0.
  p.pose.position.y = 0.
  p.pose.position.z = -0.01
  scene.add_box("groundplane", p, (2, 2, 0.009))
 
  ## Planning to a Pose goal
  ## ^^^^^^^^^^^^^^^^^^^^^^^
  ## We can plan a motion for this group to a desired pose for the
  ## end-effector
  print "============ Generating plan 1"
 
  group.set_joint_value_target([1.57,0.,0.,0.])
 
 
  ## Let's setup the planner
  group.set_planning_time(2.0)
  group.set_goal_orientation_tolerance(1)
  group.set_goal_tolerance(1)
  group.set_goal_joint_tolerance(0.1)
  group.set_num_planning_attempts(20)
 
  ## Now, we call the planner to compute the plan
  ## and visualize it if successful
  ## Note that we are just planning, not asking move_group
  ## to actually move the robot
  #group.set_goal_position_tolerance(1.5)
  plan1 = group.plan()
 
  print "============ Waiting while RVIZ displays plan1..."
  rospy.sleep(0.5)
 
 
  ## You can ask RVIZ to visualize a plan (aka trajectory) for you.  But the
  ## group.plan() method does this automatically so this is not that useful
  ## here (it just displays the same trajectory again).
  print "============ Visualizing plan1"
  display_trajectory = moveit_msgs.msg.DisplayTrajectory()
 
  display_trajectory.trajectory_start = robot.get_current_state()
  display_trajectory.trajectory.append(plan1)
  display_trajectory_publisher.publish(display_trajectory);
 
  print "============ Waiting while plan1 is visualized (again)..."
  rospy.sleep(0.5)
 
 
  ## Moving to a pose goal
  ## ^^^^^^^^^^^^^^^^^^^^^
  group.go(wait=True)
 
  ## second movement
  ## ^^^^^^^^^^^^^^^^^^^^^
 
 
  group.set_joint_value_target([0.,0.,0.,0.])
 
  plan1 = group.plan()
 
  rospy.sleep(0.5)
 
  display_trajectory = moveit_msgs.msg.DisplayTrajectory()
 
  display_trajectory.trajectory_start = robot.get_current_state()
  display_trajectory.trajectory.append(plan1)
  display_trajectory_publisher.publish(display_trajectory);
 
  rospy.sleep(0.5)
 
  group.go(wait=True)
 
  ## When finished shut down moveit_commander.
  moveit_commander.roscpp_shutdown()
 
  ## END_TUTORIAL
 
  print "============ STOPPING"
 
  R = rospy.Rate(10)
  while not rospy.is_shutdown():
    R.sleep()
 
if __name__=='__main__':
  try:
    move_group_python_interface_tutorial()
  except rospy.ROSInterruptException:
    pass