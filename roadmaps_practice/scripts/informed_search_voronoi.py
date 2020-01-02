#!/usr/bin/env python

import copy
import math
import heapq
import rospy
import random
from nav_msgs.msg import OccupancyGrid
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped


start = [45, 80]
goal = [88, 17]

# Node class to hold the location and parent node (needed for getting final path)
class Node:

	def __init__(self, value, par):
		self.value 	= value
		self.parent     = par
		self.g 		= 0.0
		self.h 		= 0.0
		self.f 		= 0.0

	def setG(self, gCost):
		self.g = self.parent.g + gCost

	def setF(self):
		self.f = self.g + self.h


class AStar:
    def __init__(self):
        self.grid = []
        self.gridData = []

        self.sub_voronoi = rospy.Subscriber('/voronoi_map', OccupancyGrid, self.VoronoiCb)

        self.pub = rospy.Publisher('/path', Path, queue_size=10)
        self.pub_sg = rospy.Publisher('marked_grid', OccupancyGrid, queue_size=10)

    def gridCb(self, msg):
        print 'In gridCb'


    def findStartOnVor(self):
        
        openList = [start]

        while not rospy.is_shutdown():
            print 'In while'

            current = openList.pop()

            neighbors = self.getNeighbors(current, self.grid)
            for n in neighbors:
                if self.grid[n] == 0:
                    return n
                else:
                    openList.append(n)


    def fsov(self, start, goal):
        print 'In fsov'
        min_dist_s = 1000000
        min_dist_g = 1000000
        qs = -1
        qg = -1
        for i in range(0, len(self.grid)):
            if self.grid[i] == 0:
                x = i % self.gridInfo.width
                y = i / self.gridInfo.width

                dist_s = abs( start[1] - x ) + abs( start[0] - y )
                dist_g = abs( goal[1] - x ) + abs( goal[0] - y )
                #print 'i: %s p: (%s,%s) dist_s: %s dist_g: %s' % (i, x, y, dist_s, dist_g)

                if dist_s < min_dist_s:
                    qs = [y, x]
                    min_dist_s = dist_s

                if dist_g < min_dist_g:
                    qg = [y, x]
                    min_dist_g = dist_g
                
        return qs, qg

    def VoronoiCb(self, msg):
        self.grid = msg.data
        self.gridInfo = msg.info
        self.maxRows = self.gridInfo.height * self.gridInfo.resolution
        self.maxCols = self.gridInfo.width * self.gridInfo.resolution

        #start = [random.randint(0, self.gridInfo.height-1), random.randint(0, self.gridInfo.width-1)]
        start = [0, 0]
        goal = [random.randint(0, self.gridInfo.height-1), random.randint(0, self.gridInfo.width-1)]
        #i_start = (start[0] * self.gridInfo.width) + start[1]
        i_start = 0
        i_goal = (goal[0] * self.gridInfo.width) + goal[1]
        
        print 'Initial start: %s grid[start]: %s' % (start, self.grid[i_start])
        print 'Initial goal: %s grid[goal]: %s' % (goal, self.grid[i_goal])

        print 'Finding start...'
        #while not rospy.is_shutdown() and self.grid[i_start] == 0:
            #start[0] = random.randint(0, self.gridInfo.height-1)
            #start[1] = random.randint(0, self.gridInfo.width-1)
            #i_start = (start[0] * self.gridInfo.width) + start[1]
        
        print 'Finding goal...'
        while not rospy.is_shutdown() and self.grid[i_goal] == 0:
            goal[0] = random.randint(0, self.gridInfo.height-1)
            goal[1] = random.randint(0, self.gridInfo.width-1)
            i_goal = (goal[0] * self.gridInfo.width) + goal[1]

        print 'start: %s goal: %s' % (start, goal)

        
        self.newGrid = OccupancyGrid()
        self.newGrid.info = msg.info

        #start = [3, 6]
        #goal = [95, 90]

        qs,qg = self.fsov(start, goal)
        print 'qs: %s qg: %s' % (qs, qg)

        i_qs = (qs[0] * msg.info.width) + qs[1]
        i_qg = (qg[0] * msg.info.width) + qg[1]

        for i in range(0,len(self.grid)):
            if i == i_start:
                self.newGrid.data.append( 50 )
            elif i == i_goal:
                self.newGrid.data.append( 50 )
            elif i == i_qs:
                self.newGrid.data.append( 50 )
            elif i == i_qg:
                self.newGrid.data.append( 50 )
            else:
                self.newGrid.data.append( self.grid[i] )
        
        self.pub_sg.publish(self.newGrid)


        t_start = rospy.Time.now()
        [p, num] = self.informedSearch('astar', self.grid, qs, qg)
        d_search = rospy.Time.now() - t_start
        print d_search.to_sec()
        print 'path: %s' % p
        print 'num_expanded: %s' % num


        # Make a nav_msgs.Path object
        path = Path()
        s = PoseStamped()
        s.pose.position.x = start[1]*self.gridInfo.resolution
        s.pose.position.y = start[0]*self.gridInfo.resolution
        path.poses.append(s)
        
        '''
        st = PoseStamped()
        st.pose.position.x = qs[0]*self.gridInfo.resolution
        st.pose.position.y = qs[1]*self.gridInfo.resolution
        path.poses.append(st)
        print 's: %s qs: %s' % (start, qs)
        print 'Converted: s: %s\nqs: %s' % (s.pose.position, st.pose.position)
        '''

        for pos in p:
            temp = PoseStamped()
            temp.pose.position.x = pos[1] * self.gridInfo.resolution
            temp.pose.position.y = pos[0] * self.gridInfo.resolution

            path.poses.append(temp)
        g = PoseStamped()
        g.pose.position.x = goal[1]*self.gridInfo.resolution
        g.pose.position.y = goal[0]*self.gridInfo.resolution
        path.poses.append(g)

        path.header.frame_id = 'map'
        print 'Publishing path...'
        self.pub.publish(path)




    # Returns false if not in the openList
    # Else, returns the existing element so that it can be easily replaced
    def InOpenList(self, node, openList):
            for n in openList:
                    if n[1].value == node.value:
                            #print 'node %s is equal to existing node in open list %s' % (node.value, n[1].value)
                            #print 'node.g: %s n.g: %s' % (node.g, n[1].g)
                            return n
            return False


    def InClosedList(self, node, closedList):
            for n in closedList:
                    if n.value == node.value:
                            return True
            return False
    
    # Returns all adjacent locations for node that are free space
    def getNeighbors(self, location, grid):

            freeVal = 0

            result = []

            i_loc = (location[0]*self.gridInfo.width)+location[1]
            #print 'len(grid.data): %s' % len(grid)
            #print 'Loc: %s i_loc: %s' % (location, i_loc)

            # Use location[:] to get a copy of the list
            # For each direction (u,r,d,l), check the bounds and value on the grid
            # Clockwise order -> u, r, d, l

            i_up = i_loc - self.gridInfo.width
            up = location[:]
            up[0] -= 1
            #print 'Up: %s i_up: %s grid[i_up]: %s' % (up, i_up, self.grid[i_up])
            if up[0] > 0 and self.grid[i_up] == freeVal:
                    result.append(up)

            i_upr = i_up + 1
            upr = location[:]
            upr[0] -= 1
            upr[1] += 1
            #print 'upr: %s i_upr: %s grid[i_upr]: %s' % (upr, i_upr, self.grid[i_upr])
            if upr[0] > 0 and upr[1] < self.gridInfo.width and self.grid[i_upr] == freeVal:
                result.append(upr)


            i_upl = i_up - 1
            upl = location[:]
            upl[0] -= 1
            upl[1] -= 1
            #print 'upl: %s i_upl: %s grid[i_upl]: %s' % (upl, i_upl, self.grid[i_upl])
            if upl[0] > 0 and upl[1] > 0 and self.grid[i_upl] == freeVal:
                result.append(upl)

            i_right = i_loc+1
            right = location[:]
            right[1] += 1
            #print 'right: %s i_right: %s grid[i_right]: %s' % (right, i_right, self.grid[i_right])
            if right[1] < self.gridInfo.width and grid[i_right] == freeVal:
                    result.append(right)


            i_down = i_loc + self.gridInfo.width
            down = location[:]
            down[0] += 1
            #print 'down: %s i_down: %s grid[i_down]: %s' % (down, i_down, self.grid[i_down])
            if down[0] < self.gridInfo.height and grid[i_down] == freeVal:
                    result.append(down)
            
            i_downr = i_down + 1
            downr = location[:]
            downr[0] += 1
            downr[1] += 1
            #print 'downr: %s i_downr: %s grid[i_downr]: %s' % (downr, i_downr, self.grid[i_downr])
            #print 'maxRows: %s maxCols: %s' % (self.maxRows, self.maxCols)
            if downr[0] < self.gridInfo.height and downr[1] < self.gridInfo.width and grid[i_downr] == freeVal:
                result.append(downr)
            
            i_downl = i_down - 1
            downl = location[:]
            downl[0] += 1
            downl[1] -= 1
            #print 'downl: %s i_downl: %s grid[i_downl]: %s' % (downl, i_downl, self.grid[i_downl])
            if downl[0] < self.gridInfo.height and downl[1] > 0 and grid[i_downl] == freeVal:
                result.append(downl)

            i_left = i_loc - 1
            left = location[:]
            left[1] -= 1
            #print 'left: %s i_left: %s grid[i_left]: %s' % (left, i_left, self.grid[i_left])
            if left[1] > -1 and grid[i_left] == freeVal:
                    result.append(left)

            #print 'up: %s down: %s left: %s right: %s' % (up, down, left, right)
            #print 'result: %s' % result

            return result


    def heuristic(self, node, goal):

            # 2D Euclidean distance
            #d = math.sqrt( math.pow(node.value[0] - goal[0], 2) + math.pow(node.value[1] - goal[1], 2) )

            # Manhattan distance
            d = abs(node.value[0] - goal[0]) + abs(node.value[1] - goal[1])
            return d




    def informedSearch(self, type, grid, start, goal):
            print '\nIn informedSearch'
            print 'type: %s start: %s goal: %s' % (type, start, goal)

            # Initialize stuff
            path = []
            numExpanded = 0
            current = Node(start, '')
            current.g = 0
            current.h = self.heuristic(current, goal)
            current.setF();

            # List of nodes to expand
            openList = []
            if type == 'astar':
                    heapq.heappush(openList, (current.f, current))
            else:
                    heapq.heappush(openList, (current.h, current))

            # List of expanded nodes
            closedList = []

            print 'Initial node: current.value: %s current.g: %d current.h: %d current.f: %d' % (current.value, current.g, current.h, current.f)

            # *** Main loop  ***
            # While we are not at the goal and we haven't expanded all nodes
            while current.value != goal and openList:
                    t_startIter = rospy.Time.now()

                    #print 'Open list size: %s' % len(openList)
                    # Pop off closed list
                    t_start = rospy.Time.now()
                    current = heapq.heappop(openList)[1]
                    #print 'current: %s current.g: %s current.h: %s' % (current.value, current.g, current.h)
                    d_pop = rospy.Time.now()-t_start
                    #print 'd_pop: %s' % d_pop.to_sec()
                    t_start = rospy.Time.now()
                    closedList.append(current)
                    d_append = rospy.Time.now() - t_start
                    #print 'd_appendClos: %s' % d_append.to_sec()
                    #print 'current.value: %s current.g: %s current.h: %s current.f: %s' % (current.value, current.g, current.h, current.f)
                    #print 'len(openList): %s' % len(openList)

                    # Check for goal
                    if current.value != goal:

                            # Get neighbors
                            t_start = rospy.Time.now()
                            neighbors = self.getNeighbors(current.value, grid)
                            d_nei = rospy.Time.now() - t_start
                            #print 'd_nei: %s' % d_nei.to_sec()

                            # For each neighbor, create node, check if duplicate, and push on
                            for n in neighbors:
                                    #print 'n: %s' % n

                                    # Create new node
                                    nd = Node(n, current)

                                    t_start = rospy.Time.now()
                                    # If greedy search, add to open list without checking closed list
                                    if type == 'greedy':

                                            # Set node values (only heuristic value for greedy search)
                                            nd.h = self.heuristic(nd, goal)
                                            heapq.heappush(openList, (nd.h, nd))

                                    # else if astar, then first check that node is not in the closed list
                                    elif not self.InClosedList(nd, closedList):
                                            #print 'Not in closed list'
                                            d_checkClos = rospy.Time.now() - t_start
                                            #print 'd_checkClos: %s' % d_checkClos.to_sec()

                                            # Set node values
                                            nd.setG(1)
                                            t_start = rospy.Time.now()
                                            nd.h = self.heuristic(nd, goal)
                                            d_heur = rospy.Time.now() - t_start
                                            #print 'd_heur: %s' % d_heur.to_sec()
                                            nd.setF()

                                            # Check if it's in the open list
                                            t_start = rospy.Time.now()
                                            o = self.InOpenList(nd, openList)
                                            d_checkOpen = rospy.Time.now() - t_start
                                            #print 'd_checkOpen: %s' % d_checkOpen.to_sec()

                                            # If not in the open list, then add it
                                            if not o:
                                                    #print 'Not in open list, adding'
                                                    t_start = rospy.Time.now()
                                                    heapq.heappush(openList, (nd.f, nd))
                                                    d_push = rospy.Time.now() - t_start
                                                    #print 'd_push: %s' % d_push.to_sec()

                                            # Else, check if the existing node should be replaced (based on path cost) 
                                            # only do this in a* because in greedy the node cost will always be the same
                                            else:
                                                    #print 'In open list'
                                                    if nd.g < o[1].g:
                                                            #print 'Updating'
                                                            o = nd
                                                            t_start = rospy.Time.now()
                                                            heapq.heapify(openList)
                                                            d_heapify = rospy.Time.now() - t_start
                                                            #print 'd_heapify: %s' % d_heapify

                                            
                            # Data
                            numExpanded += 1
                            d_iter = rospy.Time.now() - t_startIter
                            #print 'd_iter: %s' % d_iter.to_sec()
            

            # If we found the goal, then build the final path
            if current.value == goal:

                    # While not at the root, insert each node's parent
                    while current.parent != '':
                            path.insert(0,current.parent.value)
                            current = current.parent

                    # Append the goal
                    path.append(goal)
            else:
                print 'No path found'

            return [path, numExpanded]




# The grid values must be separated by spaces, e.g.
# 1 1 1 1 1 
# 1 0 0 0 1
# 1 0 0 0 1
# 1 1 1 1 1
# Returns a 2D list of 1s and 0s
def readGrid(filename):
	#print('In readGrid')
	grid = []
	with open(filename) as f:
		for l in f.readlines():
			grid.append([int(x) for x in l.split()])
	
	f.close()
	#print 'Exiting readGrid'
	return grid


# Writes a 2D list of 1s and 0s with spaces in between each character
# 1 1 1 1 1 
# 1 0 0 0 1
# 1 0 0 0 1
# 1 1 1 1 1
def outputGrid(grid, start, goal, path):
	#print 'In outputGrid'
	filenameStr = 'path.txt'

	# Open filename
	f = open(filenameStr, 'w')

	# Mark the start and goal points
	grid[start[0]][start[1]] = 'S'
	grid[goal[0]][goal[1]] = 'G'

	# Mark intermediate points with *
	for i, p in enumerate(path):
		if i > 0 and i < len(path)-1:
			grid[p[0]][p[1]] = '*'

	# Write the grid to a file
	for r, row in enumerate(grid):
		for c, col in enumerate(row):
			
			# Don't add a ' ' at the end of a line
			if c < len(row)-1:
				f.write(str(col)+' ')
			else:
				f.write(str(col))

		# Don't add a '\n' after the last line
		if r < len(grid)-1:
			f.write("\n")

	# Close file
	f.close()
	#print 'Exiting outputGrid'



def main():

    rospy.init_node('astar', anonymous=False)

    astar = AStar()
    rospy.spin()

    #[p, numExpanded] = informedSearch(algo, grid, [1, 1], [3, 7])
    #outputGrid(grid, [1,1], [3,7], p)



if __name__ == '__main__':
	main()
	print('\nExiting normally')
