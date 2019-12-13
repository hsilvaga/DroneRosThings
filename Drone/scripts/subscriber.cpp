#include <ros/ros.h>
#include <geometry_msgs/PoseStamped.h>
#include <nav_msgs/Odometry.h>




double z = 0.0;
geometry_msgs::PoseStamped states;


void stateCall(const nav_msgs::Odometry::ConstPtr& msg) {
	z = msg->pose.pose.position.z;
	ROS_INFO("z: %f", z);
}


int main(int argc, char **argv) {
	ros::init(argc,argv, "SubscribeTest");
	ros::NodeHandle w;

	ros::Rate rate(30);


	while(ros::ok()) {
		ros::Subscriber stateSub = w.subscribe("/mavros/local_position/odom",10, stateCall);

		ROS_INFO("Z: %f", z);


		ros::spin();
		rate.sleep();
	}
}
