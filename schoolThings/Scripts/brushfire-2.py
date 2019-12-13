#!/usr/bin/env python
import rospy
from nav_msgs.msg import OccupancyGrid
from roadmaps_practice.msg import GridInfo, ObPixels
width = 0
height = 0
data = GridInfo()
grid_test = OccupancyGrid()
def brushfire():
	#nav_msgs/OccupancyGrid
	global grid_test
	rospy.init_node("brushfire",anonymous = True)
	rospy.Subscriber("/mapInfo",GridInfo,callBack)
	rospy.spin()
			
def callBack(grid):
	global grid_test
	#rospy.loginfo(grid)
	data = grid
	#rospy.loginfo(grid.grid.data)
	#rospy.loginfo(grid.obs[0].i_pixels)
	#rospy.loginfo(grid.obs[1].i_pixels)
	#rospy.loginfo(grid_test.info.width)
	#rospy.loginfo(grid_test.info.height)
	width = grid.grid.info.width
	height = grid.grid.info.height
	resolution = grid.grid.info.resolution
	rospy.loginfo(width)
	index = 0
	index_data = 0
	data = []
	for r in range(0,width):
        	for c in range(0,height):
			data.append(grid.grid.data[index]),
			#print data[index],  
			index = index +1
		print "\n"
	#print cell_row
	#print cell_colom
	index = 0
	check = 1
	check_data = 100
	flag = True
	for r in range(0,width):
        		for c in range(0,height):
				#up
				if(r==0):
					data[index]= 1
				#down
				if (r==height -1):
					data[index] = 1
				#left
				if (c==0):
					data[index]=1
				if (c==width-1):
					data[index]=1
				#print data[index],  
				index = index +1
			print "\n" 
	check = 1
	check_data = 100
	flag = True
 	
	while(flag):
		a =0
		index = 0
		print check_data
		for r in range(0,width):
        		for c in range(0,height):
				#print index
				if(data[index]==0):
					a = a+1
				index = index+1
		#print a
		if (a==0):
			flag = False
		
		index = 0
		if(flag):
			for r in range(0,width):
				for c in range(0,height):
					if(data[index] == check_data):
					#	print index
					#check up
						if(index - width>0):
							if(data[index - width]==0):
								data[index-width] =check
					#check down
						if (index + width) < width*height:
							if (data[index + width]==0):
								data[index + width]=check
					#check right
						if(index+1) <width*height:
							if (data[index + 1]==0):
								data[index+1]=check
					#chekc left
						if (data[index -1]==0):
							data[index-1]=check
					#lef d 
						if (index-width -1>0):
							if (data[index-width -1]==0):
								data[index-width -1] = check
					# rigt d
						if (index-width +1>0):
							if (data[index-width +1]==0):
								data[index-width +1] = check
					#lef d
						if (index + width-1) < width*height:
							if (data[index+width -1]==0):
								data[index+width -1] = check
					# rigt d 
						if (index + width+1) < width*height:
							if (data[index+width +1]==0):
								data[index+width +1] = check
					#print data[index],  
					index = index +1
				print "\n"
		check_data = check
		check = check +1
	index = 0
	for r in range(0,width):
        		for c in range(0,height):
				if(data[index]==100):
					data[index]  = 0
				print data[index], 
				index = index +1
			print "\n" 
	pub = rospy.Publisher("/brushfire_map",OccupancyGrid,queue_size=100)
	grid_test = OccupancyGrid()
	grid_test.info.width =width
	grid_test.info.height =height
	grid_test.info.resolution =resolution
	grid_test.data=data
	rospy.sleep(0.5)
	pub.publish(grid_test)













if __name__ == '__main__':
	brushfire()
