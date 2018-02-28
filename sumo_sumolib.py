import sys
import sumolib

from settings import TOOLS_DIR

sys.path.append(TOOLS_DIR)


# parse the net
net = sumolib.net.readNet('map1/map.net.xml')

edge = net.getEdge('-324484359#1')
print (edge.getType())