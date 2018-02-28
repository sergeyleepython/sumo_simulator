import sys
import traci
import traci.constants as tc
import sumolib
from settings import TOOLS_DIR, MAP_NET_XML, MAP_SUMO_CFG

from sumo_osm_parse import get_road_quality

sys.path.append(TOOLS_DIR)

# if 'SUMO_HOME' in os.environ:
#     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
#     sys.path.append(tools)
# else:
#     sys.exit("please declare environment variable 'SUMO_HOME'")


sumoBinary = "/usr/bin/sumo-gui"
sumoCmd = [sumoBinary, "-c", MAP_SUMO_CFG]

# Then you start the simulation and connect to it with your script:


# traci.start(sumoCmd)
# step = 0
# while step < 1000:
#     traci.simulationStep()
#     if traci.inductionloop.getLastStepVehicleNumber("0") > 0:
#         traci.trafficlight.setRedYellowGreenState("0", "GrGr")
#     step += 1
#
# traci.close()


# Subscription
# Subscriptions can be thought of as a batch mode for retrieving variables.
# Instead of asking for the same variables over and over again, you can retrieve the values of interest automatically after each time step.
# TraCI subscriptions are handled on a per module basis.
# That is you can ask the module for the result of all current subscriptions after each time step.
# In order to subscribe for variables you need to know their variable ids which can be looked up in the traci/constants.py file.

net = sumolib.net.readNet(MAP_NET_XML)
suv_1 = "suv_1"
truck_1 = "truck_1"
traci.start(["sumo", "-c", MAP_SUMO_CFG])
simulation = traci.simulation
vehicle = traci.vehicle
for step in range(100):
    print("step", step)
    traci.simulationStep()
    road_id = vehicle.getRoadID(suv_1)
    road_id = road_id.strip('-').strip(':').split('#')[0]
    road_id = int(road_id)
    print(road_id)
    road_quality = get_road_quality(road_id)
    print(road_quality)
    x, y = vehicle.getPosition(suv_1)
    lon, lat = net.convertXY2LonLat(x, y)
    print(lat, lon)
    distance1 = vehicle.getDistance(suv_1)
    print(distance1)
    sim_time = simulation.getCurrentTime()
    print(sim_time)
traci.close()
# elevation
# https://maps.googleapis.com/maps/api/elevation/json?locations=48.76031971084903,55.726867507763444
