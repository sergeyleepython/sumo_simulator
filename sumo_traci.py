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

    speed_truck = vehicle.getSpeed(truck_1) * 3.6
    print('Speed', speed_truck)

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

    x_truck, y_truck = vehicle.getPosition(truck_1)
    lon_truck, lat_truck = net.convertXY2LonLat(x_truck, y_truck)
    print(lat_truck, lon_truck)

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

    data_for_mqtt = {"timestamp": int(datetime.datetime.now().timestamp() * 1000),
                     "mission_id": 1,
                     "vehicle_id": 1,
                     "location": {
                         "lat": lat,
                         "lon": lon,
                         "alt": 104
                     },
                     "sensors": {
                         "speed": str(speed) + 'km\/h',
                         "barometric_pressure": '98kPa',
                         "engine_coolant_temp": '96C',
                         "fuel-level": 'NODATA',
                         "engine_load": '31,8%',
                         "ambient_air_temp": '9C',
                         "engine-rpm": "748RPM",
                         "intake_manifold_pressure": "NODATA",
                         "maf": "3,66g\/s",
                         "long-term-fuel-trim-bank-2": "NODATA",
                         "fuel-type": "NODATA",
                         "air_intake_temp": "28C",
                         "fuel-pressure": "NODATA",
                         "short-term-fuel-trim-bank-2": "NODATA",
                         "short-term-fuel-trim-bank-1": "-2,3%",
                         "engine-runtime": "00:17:07",
                         "throttle-pos": "12,9%",
                         "dtc-number": "MIL is OFF0 codes",
                         "trouble-codes": "C0300\n",
                         "timing-advance": "59,6%",
                         "equiv-ratio": "1,0%"
                     },
                     # "road_condition": road_attrs
                     }

    data_for_mqtt = {"timestamp": int(datetime.datetime.now().timestamp() * 1000), "mission_id": 1, "vehicle_id": 1,
                     "location": {"lon": lon, "lat": lat, "alt": 145},
                     "sensors": [{"slug": "barometric-pressure", "warning": True, "value": "0"},
                                 {"slug": "engine-coolant-temp", "warning": False, "value": "-40.0"},
                                 {"slug": "fuel-level", "warning": True, "value": "0.0"},
                                 {"slug": "engine-load", "warning": True, "value": "0.0"},
                                 {"slug": "ambient-air-temp", "warning": True, "value": "-40.0"},
                                 {"slug": "engine-rpm", "warning": True, "value": "0"},
                                 {"slug": "intake-manifold-pressure", "warning": True, "value": "0"},
                                 {"slug": "maf", "warning": True, "value": "0.0"},
                                 {"slug": "term-fuel-trim-bank-1", "warning": False},
                                 {"slug": "fuel-economy", "warning": False},
                                 {"slug": "long-term-fuel-trim-bank-2", "warning": True, "value": "-100.0"},
                                 {"slug": "fuel-type", "warning": True, "value": "0"},
                                 {"slug": "air-intake-temp", "warning": True, "value": "-40.0"},
                                 {"slug": "fuel-pressure", "warning": True, "value": "0"},
                                 {"slug": "speed", "warning": True, "value": str(speed)},
                                 {"slug": "short-term-fuel-trim-bank-2", "warning": True, "value": "-100.0"},
                                 {"slug": "short-term-fuel-trim-bank-1", "warning": True, "value": "-100.0"},
                                 {"slug": "engine-runtime", "warning": True, "value": "0"},
                                 {"slug": "throttle-pos", "warning": True, "value": "0.0"},
                                 {"slug": "dtc-number", "warning": True, "value": "MIL is OFF0 codes"},
                                 {"slug": "trouble-codes", "warning": False, "value": "C0300\n"},
                                 {"slug": "timing-advance", "warning": True, "value": "0.0"},
                                 {"slug": "equiv-ratio", "warning": True, "value": "0.0"}]}

    data_for_mqtt_truck = {"timestamp": int(datetime.datetime.now().timestamp() * 1000), "mission_id": 1,
                           "vehicle_id": 2,
                           "location": {"lon": lon_truck, "lat": lat_truck, "alt": 145},
                           "sensors": [{"slug": "barometric-pressure", "warning": True, "value": "0"},
                                       {"slug": "engine-coolant-temp", "warning": False, "value": "-40.0"},
                                       {"slug": "fuel-level", "warning": True, "value": "0.0"},
                                       {"slug": "engine-load", "warning": True, "value": "0.0"},
                                       {"slug": "ambient-air-temp", "warning": True, "value": "-40.0"},
                                       {"slug": "engine-rpm", "warning": True, "value": "0"},
                                       {"slug": "intake-manifold-pressure", "warning": True, "value": "0"},
                                       {"slug": "maf", "warning": True, "value": "0.0"},
                                       {"slug": "term-fuel-trim-bank-1", "warning": False},
                                       {"slug": "fuel-economy", "warning": False},
                                       {"slug": "long-term-fuel-trim-bank-2", "warning": True, "value": "-100.0"},
                                       {"slug": "fuel-type", "warning": True, "value": "0"},
                                       {"slug": "air-intake-temp", "warning": True, "value": "-40.0"},
                                       {"slug": "fuel-pressure", "warning": True, "value": "0"},
                                       {"slug": "speed", "warning": True, "value": str(speed_truck)},
                                       {"slug": "short-term-fuel-trim-bank-2", "warning": True, "value": "-100.0"},
                                       {"slug": "short-term-fuel-trim-bank-1", "warning": True, "value": "-100.0"},
                                       {"slug": "engine-runtime", "warning": True, "value": "0"},
                                       {"slug": "throttle-pos", "warning": True, "value": "0.0"},
                                       {"slug": "dtc-number", "warning": True, "value": "MIL is OFF0 codes"},
                                       {"slug": "trouble-codes", "warning": False, "value": "C0300\n"},
                                       {"slug": "timing-advance", "warning": True, "value": "0.0"},
                                       {"slug": "equiv-ratio", "warning": True, "value": "0.0"}]}

    json_data = json.dumps(data_for_mqtt)
    print(json_data)
    # publish_to_mqtt(topic="test", data=json_data)

    # time.sleep(1)

    json_data_truck = json.dumps(data_for_mqtt_truck)
    print(json_data_truck)

    result = [
        json_data,
        json_data_truck
    ]

    return result  # traci.close()

# elevation
# https://maps.googleapis.com/maps/api/elevation/json?locations=48.76031971084903,55.726867507763444
