#include <ros/ros.h>
#include "setup.h"
#include <nav_msgs/Odometry.h>
#include <geometry_msgs/TwistStamped.h>
#include <geometry_msgs/PoseStamped.h>

std::string Drone_Name;




int main(int argc, char **argv) {
	ros::init(argc,argv, "Transform_Test");

	Drone_Name = argv[24];
	printf("%s", Drone_Name);



	return 0;
}
