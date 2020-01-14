#!/usr/bin/env python

from std_msgs.msg import String
from std_msgs.msg import UInt32
import rospy

def callbackB(data):
    print("Here be numbers from topic b: %i", data)

def callbackA(data):
    print("Here be words from topic a: %s", data)

def main():
    print("Listening")
    while not rospy.is_shutdown():
        rospy.Subscriber("topic_a", String, callbackA)
        rospy.Subscriber("topic_b", UInt32, callbackB)
        rate.sleep()

if __name__=="__main__":
    rospy.init_node("node_c")
    rate = rospy.Rate(10)
    main()

