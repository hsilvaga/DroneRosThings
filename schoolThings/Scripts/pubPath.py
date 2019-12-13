#!/usr/bin/env python
import rospy
import random
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped


def generatePath(numPoints):
    result = Path()
    result.header.frame_id="odom"

    for i in range(0,numPoints):
        print i
        
        p = PoseStamped()
        
        dx = random.randrange(1,5) * 0.1
        dy = random.randrange(1,5) * 0.1
        print 'dx: %s dy: %s' % (dx, dy)

        if i > 0:
            p.pose.position.x = result.poses[i-1].pose.position.x + dx
            p.pose.position.y = result.poses[i-1].pose.position.y + dy
        else:
            p.pose.position.x = 0
            p.pose.position.y = 0


        print 'Point %s: (%s,%s)' % (i, p.pose.position.x, p.pose.position.y)
        

        result.poses.append(p)



    return result
    


def main():
    print 'In main'
    rospy.init_node('pubPath', anonymous=True)

    pub_path = rospy.Publisher('/path', Path, queue_size=10)

    path = generatePath(5)

    raw_input('Press enter to publish the path.')
    initSleep = rospy.Duration(1)
    rospy.sleep(initSleep)

    # Publish the path
    pub_path.publish(path)


    print 'Exiting normally'

if __name__ == '__main__':
    main()

