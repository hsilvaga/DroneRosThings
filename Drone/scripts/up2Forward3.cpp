/*
 * @description This program:
 * 		*Sets the mode of the drone to OFFBOARD
 * 		*Arms the drone
 * 		*Moves it up in the z direction
 * 		*Moves it forward in the x direction
 */

#include <ros/ros.h>
#include "setup.h"
#include <nav_msgs/Odometry.h>
#include <geometry_msgs/TwistStamped.h>
#include <geometry_msgs/PoseStamped.h>


nav_msgs::Odometry odomData;
ros::Publisher posePub1;

double poseX = 0.0;
double poseY = 0.0;
double poseZ = 0.0;


/*
 * @description Moves(also publishes) to specified coordinates
 * 		@param x, y, z
 */
geometry_msgs::PoseStamped twistMsg;
void move(double x, double y, double z) {
	twistMsg.pose.position.x = x;
	twistMsg.pose.position.y = y;
	twistMsg.pose.position.z = z;

	posePub1.publish(twistMsg);
}

/*
 * @description call back for Odometry messages
 * sets up x, y, z position data
 */
void odomCall(const nav_msgs::Odometry::ConstPtr& msg) {
	poseX = msg ->pose.pose.position.x;
	poseY = msg ->pose.pose.position.y;
	poseZ = msg ->pose.pose.position.z;

	odomData = *msg;
}

int main(int argc, char **argv) {
	ros::init(argc, argv, "FirstMove");
	ros::NodeHandle h;
	setupc Set;
	ros::Rate rate(30);
	bool breakOut = true;

	posePub1 = h.advertise<geometry_msgs::PoseStamped>
				("/mavros/setpoint_position/local",100);

	Set.setup(argc, argv);
	Set.setMode();
	Set.setArm(true);

	while(ros::ok() && breakOut) {

		ros::Subscriber odomSub = h.subscribe<nav_msgs::Odometry>
										("/mavros/local_position/odom", 100, odomCall);

		//Move up 5 meters
		while(poseZ <= 5.0 && ros::ok()) {
			move(0.0,0.0,5.1);

			ROS_INFO("Moving. Z = %f", poseZ);

			ros::spinOnce();
			rate.sleep();
		}
		ROS_INFO("Reached 5 meters");

		//Move forward 4 meters
		while(poseX < 4 && ros::ok()) {
			ROS_INFO("X: %f Z: %f", poseX, poseZ);
			move(4.0, 0.0, 5.0);


			ros::spinOnce();
			rate.sleep();
		}
		ROS_INFO("X: 4 / Z: 5 reached!");
		breakOut = false; //Breaks out of the program
		rate.sleep();
	}


	return 0;
}
