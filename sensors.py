import random

# Возможно это нужно сделать классом, чтобы сохранять предыдущие значения и передавать третьим аргументом в функции.

def barometric_pressure(timestamp, speed):
    return random.uniform(0.5, 4.5)


def engine_coolant_temp(timestamp, speed):
    return random.uniform(0.5, 40.0)


def engine_load(timestamp, speed):
    return random.uniform(0, 13)


def ambient_air_temp(timestamp, speed):
    return random.uniform(0, 13)


def intake_manifold_pressure(timestamp, speed):
    return random.uniform(0, 13)


def maf(timestamp, speed):
    return random.uniform(0, 13)


def air_intake_temp(timestamp, speed):
    return random.uniform(0, 13)


def engine_runtime(timestamp, speed):
    return random.uniform(0, 13)


def throttle_pos(timestamp, speed):
    return random.uniform(0, 13)


def battery_voltage(timestamp, speed):
    return random.uniform(0, 13)
