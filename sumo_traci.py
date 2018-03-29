import sys
import datetime
import time

import traci
# import traci.constants as tc
import sumolib

from settings import TOOLS_DIR, MAP_NET_XML, MAP_SUMO_CFG
from sumo_osm_parse import get_road_attributes
from firebase import db

sys.path.append(TOOLS_DIR)

sumoBinary = "/usr/bin/sumo-gui"
sumoCmd = [sumoBinary, "-c", MAP_SUMO_CFG]

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
    data = {}
    step += 1
    print("step", step)
    traci.simulationStep()

    speed = vehicle.getSpeed(suv_1) * 3.6
    data['speed'] = speed
    print('Speed', speed)

    accel = vehicle.getAccel(suv_1)
    data['accel'] = accel
    print('Acceleration', accel)

    road_id = vehicle.getRoadID(suv_1)
    road_id = road_id.strip('-').strip(':').split('#')[0]
    road_id = int(road_id)
    data['road_id'] = road_id
    print('Road id: {}'.format(road_id))

    road_attrs = get_road_attributes(road_id) or {}
    data = {**data, **road_attrs}
    print('Road attributes: {}'.format(road_attrs))

    x, y = vehicle.getPosition(suv_1)
    lon, lat = net.convertXY2LonLat(x, y)
    data['lat'] = lat
    data['lon'] = lon
    print(lat, lon)

    distance = vehicle.getDistance(suv_1)
    data['distance'] = distance
    print('Distance: {}'.format(distance))

    sim_time = simulation.getCurrentTime() / 1000
    data['sim_time'] = sim_time
    print('Sim time: {}'.format(sim_time))

    data = {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"): data}
    print(data)
    db.child("sensors").child("veh1-subassies-braking_system-FL_element-type1-1").update(data)
    # time.sleep(1)
traci.close()

# elevation
# https://maps.googleapis.com/maps/api/elevation/json?locations=48.76031971084903,55.726867507763444
