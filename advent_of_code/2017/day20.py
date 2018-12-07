# !/bin/python3
# http://www.adventofcode.com/2017/day/20

from utils import read_input


def collide(particle_info):
    closest = 0
    slowest = abs(sum(particle_info[0]['acceleration']))

    for particle, info in particle_info.items():
        acceleration = abs(sum(info['acceleration']))
        if acceleration > slowest:
            continue

        if acceleration < slowest:
            closest = particle
            slowest = acceleration
            continue

        # if current and slowest are using the same acceleration, use velocity as a tie breaker
        velocity = sum(info['velocity'])
        closest_vel = sum(particle_info[closest]['velocity'])

        if velocity > closest_vel:
            continue

        if velocity < closest_vel:
            closest = particle
            slowest = acceleration
            continue

        # if current and slowest are using the same velocity, use distance as a tie breaker
        position = sum(info['position'])
        closest_dist = sum(particle_info[closest]['position'])

        if position < closest_dist:
            closest = particle
            slowest = acceleration

    return closest


def dont_collide(particle_info):
    pass



def parse_particle(position, velocity, acceleration):
    return {'position': [abs(int(x)) for x in position[3:-1].split(',')],
            'velocity': [abs(int(x)) for x in velocity[3:-1].split(',')],
            'acceleration': [abs(int(x)) for x in acceleration[3:-1].split(',')]}


def get_closest(particle_info, allow_collision=False):
    if allow_collision:
        return dont_collide(particle_info)
    return collide(particle_info)


if __name__ == '__main__':
    PARTICLE_INFO = {I: parse_particle(*X) for I, X in enumerate(read_input(separator=', '))}
    print('part a:', get_closest(PARTICLE_INFO))
