from osmread import parse_file, Way
from settings import OSM_FILE

ways = {entity.id: entity.tags for entity in parse_file(OSM_FILE) if isinstance(entity, Way)}


def get_road_attributes(way_id):
    return ways.get(way_id)
