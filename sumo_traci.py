import json
import sys
import datetime

import traci
# import traci.constants as tc
import sumolib

from settings import TOOLS_DIR, MAP_NET_XML, MAP_SUMO_CFG
from sumo_osm_parse import get_road_attributes
from firebase import db
from mqtt_simple_publisher import publish_to_mqtt
from sensors import *

sys.path.append(TOOLS_DIR)

net = sumolib.net.readNet(MAP_NET_XML)
suv_1 = "suv_1"
truck_1 = "truck_1"
traci.start(["sumo", "-c", MAP_SUMO_CFG])
simulation = traci.simulation
vehicle = traci.vehicle
step = 0


def make_step():
    data = {}
    # step += 1
    # print("step", step)
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

    current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {current_timestamp: data}
    # write to firebase
    # db.child("sensors").child("veh1-subassies-braking_system-FL_element-type1-1").update(data)


    # MQTT data
    data_for_mqtt = {'timestamp': current_timestamp,
                     'mission_id': 1,
                     'driver_id': 'sergey',
                     'vehicle_id': 1,
                     'vehicle_type': 'suv',
                     'distance': distance,
                     'speed': speed,
                     'location': {'lon': lon, 'lat': lat}}

    data_for_mqtt = {"timestamp": current_timestamp,
                     "mission_id": 1,
                     "vehicle_id": 1,
                     "location": {
                         "lat": lat,
                         "lon": lon,
                         "alt": 104
                     },
                     "sensors": {
                         "speed": speed,
                         "barometric_pressure": barometric_pressure(current_timestamp, speed),
                         "engine_coolant_temp": engine_coolant_temp(current_timestamp, speed),
                         "engine_load": engine_load(current_timestamp, speed),
                         "ambient_air_temp": ambient_air_temp(current_timestamp, speed),
                         "intake_manifold_pressure": intake_manifold_pressure(current_timestamp, speed),
                         "maf": maf(current_timestamp, speed),
                         "air_intake_temp": air_intake_temp(current_timestamp, speed),
                         "engine_runtime": engine_runtime(current_timestamp, speed),
                         "throttle_pos": throttle_pos(current_timestamp, speed),
                         "trouble_codes": "C0300",
                         "battery_voltage": battery_voltage(current_timestamp, speed)
                     },
                     "road_condition": road_attrs
                     }

    json_data = json.dumps(data_for_mqtt)
    print(json_data)
    # publish_to_mqtt(topic="test", data=json_data)

    # time.sleep(1)
    return json_data  # traci.close()

# elevation
# https://maps.googleapis.com/maps/api/elevation/json?locations=48.76031971084903,55.726867507763444
