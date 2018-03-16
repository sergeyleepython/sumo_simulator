import sys
import traci
# import traci.constants as tc
import sumolib
from settings import TOOLS_DIR, MAP_NET_XML, MAP_SUMO_CFG

from sumo_osm_parse import get_road_attributes

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


# netconvert --osm-files map.osm -o map.net.xml
# polyconvert --net-file map.net.xml --osm-files map.osm --type-file typemap.xml -o map.poly.xml
# sumo-gui map.sumo.cfg

net = sumolib.net.readNet(MAP_NET_XML)
suv_1 = "suv_1"
truck_1 = "truck_1"
traci.start(["sumo-gui", "-c", MAP_SUMO_CFG])
simulation = traci.simulation
vehicle = traci.vehicle
step = 0
while True:
    try:
        step += 1
        print("step", step)
        traci.simulationStep()
        road_id = vehicle.getRoadID(suv_1)
        road_id = road_id.strip('-').strip(':').split('#')[0]
        road_id = int(road_id)
        print('Road id: {}'.format(road_id))
        road_attrs = get_road_attributes(road_id)
        print('Road attributes: {}'.format(road_attrs))
        x, y = vehicle.getPosition(suv_1)
        lon, lat = net.convertXY2LonLat(x, y)
        print(lat, lon)
        distance1 = vehicle.getDistance(suv_1)
        print('Distance: {}'.format(distance1))
        sim_time = simulation.getCurrentTime()
        print('Sim time: {}'.format(sim_time))
    except Exception as e:
        traci.close()
        raise e
traci.close()

# elevation
# https://maps.googleapis.com/maps/api/elevation/json?locations=48.76031971084903,55.726867507763444
