#!/usr/bin/env python
import rospy, math
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Point
from laser_feature_extraction.msg import LineMsg, CornerMsg
from visualization_msgs.msg import Marker
check = 0
def listennerScan():
	rospy.init_node("lines_and_corners",anonymous = True)
	rospy.Subscriber("/scan",LaserScan,callBackLaserScan)
	rospy.spin()

def callBackLaserScan(data):
	global check 
	pub = rospy.Publisher("/visualization_marker",Marker,queue_size =10)
	pointArray = []
	Array = []
	count =1
	for distance in data.ranges:
		if(not math.isnan(distance)and distance >0):
			theta = (data.angle_increment*count) + data.angle_min
			point = Point()
			point.x = distance * math.cos(theta)
			#p#rint "x", point.x
			point.y = distance*math.sin(theta)
			pointArray.append(point)
		count += 1
	getAllLines(pointArray)
	check +=1
	
def getLineBetweenPoint(start, end):
	line=Line(0,0,0,start,end,0)
	#Ax+By + C =0
	#A = slope , B = -1 , C = d
	# y = slope *x +d
	A = line.slopeLine()##
	#print A
	B = -1
	C = start.y - A*start.x
	#print C
	#y = slopx + c logi starpoint or end point to get C
	#c = start.y - slope*start.x
	#normalizing

	k = 1.0/math.sqrt(A*A+B*B)
	A = A*k
	B = B*k
	C = C*k
	#print (A**2+B**2)
	line =Line(A,B,C,start,end,0)
	return line
def getDistanceToLine(point, line):
	#formula
	#d = |Ax+By+C|/sqrt(A**2+B**2)
	#print line.A*point.x
	#print line.B*point.y
	#print line.C
	#print line.A*point.x + line.B*point.y + line.C
	#print abs(line.A*point.x + line.B*point.y + line.C)
	if(point.x - line.p_a.x ==0 or point.y - line.p_b.y and line.A ==0):
		d = 0
	else:
		d = abs(line.A*point.x + line.B*point.y + line.C)
	#print "d in get DIstamce", d
	return d
def getLine(pointArray):
	dMax = 0
	closeDistance = .15
	#print pointArray
	index = 0
	index_max =0
	pointMax = Point()
	#print "Frist", pointArray[0],pointArray[len(pointArray)-1]
	line =getLineBetweenPoint(pointArray[0], pointArray[len(pointArray)-1])
	for point in pointArray:
		distancePoint =getDistanceToLine(point, line)
		#print distancePoint 
		if( distancePoint >= dMax):
			dMax = distancePoint
			pointMax = point
			index_max = index
		index +=1
	#line =getLineBetweenPoint(pointArray[0], pointArray[index_max])
	#print "dMax",dMax
	#print pointMax
	#print "index", index
	if(dMax > closeDistance):
		#print "Dmax",dMax
		return (False,index_max)
	else:
		return (True,line)
	

def getAllLines(pointArray):
	#print "***************************************************",pointArray
	toProcess = []
	list_line = []
	list_corner = []
	#print pointArray
	(check,position) = getLine(pointArray)
	if check == False:
		toProcess.append(pointArray[:position])
		toProcess.append(pointArray[position:])
		#print "false"
		#print "false", toProcess
	else:
		list_line.append(position)
	
	number = 0
	while len(toProcess)>0:
		#print toProcess
		(check,position)=getLine(toProcess[0])
		if(len(toProcess[0])>2):
			if check == False:
				#print "false", toProcess[0]
				toProcess.append(toProcess[0][:position])
				toProcess.append(toProcess[0][position:])
				
			else:
				#print"true",position.p_a,position.p_b,toProcess[0]
				list_line.append(position)
		toProcess.remove(toProcess[0])
		number +=1
	getCornersFromLines(list_line)
	print "out"
	for i in list_line:
		list_corner.append(Corner(i.p_a))
		list_corner.append(Corner(i.p_b))
	pub = rospy.Publisher("/visualization_marker",Marker,queue_size =10)
	rospy.sleep(1)
	pub.publish(buildRvizLineList(list_line))
	#pub.publish(buildRvizCorners(list_corner))

dp = DepthFeatures()
def getCornersFromLines(lineArray):
	dp.lines = lineArray
	list_corner = []
	for l in lineArray:
		for m in lineArray:
			if (l != m):
				theta = math.atan((m.slopeLine() - l.slopeLine())/(1+m.slopeLine()*l.slopeLine()))
				theta = theta*180/math.pi
				if(theta >45 and theta <120):
					#distance 2 endpoint of line
					distance1 = math.sqrt((m.p_b.x-l.p_b.x)**2+(m.p_b.y-l.p_b.y)**2)
					distance2 = math.sqrt((m.p_a.x-l.p_a.x)**2+(m.p_a.y-l.p_a.y)**2)
					distance3 = math.sqrt((m.p_a.x-l.p_b.x)**2+(m.p_a.y-l.p_b.y)**2)
					#list_corner.append(Corner(l.p_b))
					#list_corner.append(Corner(m.p_b))
					if(distance1 < 0.2):
						print distance1
						print theta
						list_corner.append(Corner(m.p_b))
					if(distance2 <0.2):
						print distance2
						print theta
						list_corner.append(Corner(m.p_a))
					if(distance3 <0.2):
						print distance3
						print theta
						list_corner.append(Corner(m.p_a))
						#list_corner.append(Corner(l.p_b))

					"""midPoint = Point()
					if (minIndex == 0):
						midPoint.x = x.p_a.x + y.p_a.x / 2
						midPoint.y = x.p_a.y + y.p_a.y / 2
					elif (minIndex == 1):
						midPoint.x = x.p_a.y + y.p_b.x / 2
						midPoint.y = x.p_a.y + y.p_b.y / 2
					elif (minIndex == 2):
						midPoint.x = x.p_b.y + y.p_a.x / 2
						midPoint.y = x.p_b.y + y.p_a.y / 2
					elif (minIndex == 3):
						midPoint.x = x.p_b.y + y.p_b.x / 2
						midPoint.y = x.p_b.y + y.p_b.y / 2"""
	pub = rospy.Publisher("/visualization_marker",Marker,queue_size =10)
	rospy.sleep(1)
	#pub.publish(buildRvizLineList(list_line))
	pub.publish(buildRvizCorners(list_corner))
					
		



####################################
#####Class line
class Line:
	msg = LineMsg()
	A =0
	B = 0
	C = 0
	p_a = Point()
	p_b = Point()
	ID = 0
	def __init__(self, A,B,C,p_a,p_b,ID):
		self.A =A
		self.B = B
		self.C = C
		self.p_a= p_a
		self.p_b = p_b
		self.id = ID
		self.lineLength = math.sqrt((p_b.x-p_a.x)**2 +(p_b.y - p_a.y)**2)
		#print p_b.y,p_a.y,p_b.x,p_a.x
		#print float(1.0/2)
		if (p_b.x - p_a.x == 0):
			self.lineSlope = 0
		else:
			self.lineSlope = (float(p_b.y - p_a.y)/(p_b.x - p_a.x))
	def lengthLine(self):
		return self.lineLength
	def slopeLine(self):
		return self.lineSlope
	def MSG(self):
		self.msg.A = self.A
		self.msg.B = self.B
		self.msg.C = self.C
		self.msg.p_a =self.p_a
		self.msg.p_b = self.p_b
		self.msg.id = self.ID
		return self.msg
class Corner:
	msg = CornerMsg()
	l_a = LineMsg()
	l_b = LineMsg()
	def __init__(self,p,l_a=None,l_b=None):
		self.p = p
		self.l_a = l_a
		self.l_b = l_b
	def MSG(self):
		self.msg.p = p
		self.msg.l_a = l_a
		self.msg.l_b = l_b
		return self.msg

def main():
	rospy.init_node("lines_and_corners",anonymous = True)
	pub = rospy.Publisher("/visualization_marker",Marker,queue_size =10)
	#line_1 = LineMsg()
	#line_2 = LineMsg()
	coner = CornerMsg()
	pa = Point()
	pb = Point()
	pa1 = Point()
	pb1 = Point()
	list_line = []
	list_corner = []
	## line 1
	pa.x = 1
	pa.y = 1
	
	pb.x = 4
	pb.y = 5
	line_1 = Line(0,0,0,pa,pb,1)
	#print line_1.p_a
	
	##line 2
	pa1.x = 2
	pa1.y = 3
	pb1.x = -1
	pb1.y = 3
	line_2 = Line(0,0,0,pa1,pb1,0)
	list_line.append(line_1)
	list_line.append(line_2)
	#print line_1.MSG()
	#print line_2.MSG()
	#print list_line[0]
	#print list_line[1]
	##coner
	list_corner.append(Corner(pa))
	list_corner.append(Corner(pb))
	list_corner.append(Corner(pa1))
	list_corner.append(Corner(pb1))
	rospy.sleep(1)
	pub.publish(buildRvizLineList(list_line))
	#print buildRvizLineList(list_line)
	pub.publish(buildRvizCorners(list_corner))

def buildRvizLineList(lines):
 
    line_list = Marker()
    line_list.header.frame_id = 'base_scan'
    line_list.header.stamp = rospy.Time(0)
    line_list.ns = ''
 
    line_list.id = 0
    line_list.type = 5
    line_list.action = 0
   
    line_list.scale.x = 0.02
 
    line_list.color.g = 1.0
    line_list.color.a = 1.0
 
    # Add the line endpoints to list of points
    for l in lines:
        line_list.points.append(l.p_a)
        line_list.points.append(l.p_b)
   
    return line_list

def buildRvizCorners(corners):
 
    pointMarker = Marker()
    pointMarker.header.frame_id = 'base_scan'
    pointMarker.header.stamp = rospy.Time(0)
    pointMarker.ns = ''
 
    pointMarker.id = 10
    pointMarker.type = 8
    pointMarker.action = 0
   
    pointMarker.scale.x = 0.2
    pointMarker.scale.y = 0.2
    pointMarker.scale.z = 0.2
 
    pointMarker.color.b = 1.0
    pointMarker.color.a = 1.0
    pointMarker.colors.append(pointMarker.color)
 
   
    for c in corners:
        pointMarker.points.append(c.p)
 
    #pub_rviz.publish(pointMarker)
    return pointMarker

if __name__ =='__main__':
	#main()
	rospy.init_node("lines_and_corners",anonymous = True)
	listennerScan()
	list_point =[]
	array = [[1,0],[2,0],[3,0],[4,0],[5,0],[2,4],[3,3],[4,2],[5,1],[0,1],[0,2],[0,3],[0,4],[0,5],[-5,0],[-5,-1],[-5,-2],[-5,-3],[-5,-4],[-5,-5]]
	for i in array:
		#print "iiiiiiiiiiiiiiiii",i
		point_array = Point()
		point_array.x = i[0]
		point_array.y = i[1]
		list_point.append(point_array)
	Spoint = Point()
	Epoint = Point()
	point = Point()
	point1 = Point()
	Spoint.x =1
	Spoint.y = 1
	Epoint.x =4
	Epoint.y = 5
	point.x = 2
	point.y = 3
	point1.x = -1
	point.y = 2
	#getDistanceToLine(point,getLineBetweenPoint(Spoint, Epoint))
	#getAllLines(list_point)
	




