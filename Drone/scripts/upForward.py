#!/usr/bin/env python2



import rospy, time
#from mavros_msgs.msg import Pose
from geometry_msgs.msg import PoseStamped , TwistStamped
from mavros_msgs.srv import SetMode, CommandBool
from mavros_msgs.msg import AttitudeTarget, State
from MavrosSetUP import MavrosSetUP
import std_msgs.msg
from tf.transformations import quaternion_from_euler
from tf.transformations import euler_from_quaternion




def main():

    setPoints(0,0,2)
    mavrosSet.set_mode("OFFBOARD", 5)  # sets drone to offboard which is custom (0)
    mavrosSet.set_arm(True, 5)  # arms the drone

    while not rospy.is_shutdown():

        odomSubscriber()
        #move(0,0,.2)
        print("PoseZ: ", poseZ)
        if(poseZ >= 5):
            move(0,0,0)
            print("Hi")
        rate.sleep()


setPointMsg = PoseStamped()
def setPoints(x,y,z):
    for x in range(100 and not rospy.is_shutdown()):
        setPointMsg.pose.position.x = x
        setPointMsg.pose.position.y = y
        setPointMsg.pose.position.z = z
        setPointMsg.header.seq = 0
        setPointMsg.header.stamp = rospy.rostime.Time.now()
        setPointMsg.header.frame_id = '' #iris::base_link

        setPointPub.publish(setPointMsg)

        rate.sleep()

moveMsg = TwistStamped()
def move(x, y, z): #set speed
    moveMsg.twist.linear.x = x
    moveMsg.twist.linear.y = y
    moveMsg.twist.linear.z = z
    #moveMsg.thrust = 1
    #print("Publishing")
    movePub.publish(moveMsg)

def odomSubscriber():
    rospy.Subscriber('/mavros/local_position/pose', PoseStamped, poseCall)

def poseCall(data):
    global poseX
    global poseZ

    poseX = data.pose.position.x
    poseZ = data.pose.position.z


if __name__== "__main__":
    rospy.init_node('moveupForward', anonymous=True)
    movePub = rospy.Publisher('/mavros/setpoint_attitude/cmd_vel', TwistStamped, queue_size=10)
    setPointPub = rospy.Publisher('/mavros/setpoint_position/local', PoseStamped, queue_size=10)
    mavrosSet = MavrosSetUP()
    mavrosSet.setUp()

    rate = rospy.Rate(30)
    poseX = 0.0
    poseZ = 0.0


    main()



