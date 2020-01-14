#!/usr/bin/env python
from node_talk.msg import MyMsg
import rospy

def callbackA(myMsg):
    rospy.loginfo("ID: %s", myMsg.id)
    rospy.loginfo("Message: %s", myMsg.message)

def main():
    print("Listening!")
    while not rospy.is_shutdown():
        rospy.Subscriber("mymsg_a", MyMsg, callbackA)
        rate.sleep()

if __name__=="__main__":
    rospy.init_node("testing_msgs_bNode")
    rate = rospy.Rate(10)
    main()