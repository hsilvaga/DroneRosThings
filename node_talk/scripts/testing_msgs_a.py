#!/usr/bin/env python
from node_talk.msg import MyMsg
import rospy

msg = MyMsg()
def publish(id, message):
    msg.id = id
    msg.message = message
    pub.publish(msg)

def main():
    print("Publishing!")
    while not rospy.is_shutdown():
        publish(69, "Yeet")
        rate.sleep()

if __name__=="__main__":
    rospy.init_node("testing_msgs_a")
    pub = rospy.Publisher("mymsg_a", MyMsg, queue_size=10)
    rate = rospy.Rate(10)

    main()