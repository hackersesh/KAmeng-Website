import math
import numpy as np

from constants import *
from utility import *
from initial_state import get_asteroid_state
from data import main as fetch_data, store_output

TIME_COL_INDEX = 7
DIST_COL_INDEX = 8

def main():
    data = fetch_data()
    num_asteroids = len(data)
    output = []
    for x in data:
        a_coord, a_vel = get_asteroid_state(**data[x])
        # w = angular_velocity(a_coord, a_vel)
        # a_plane_normal = np.cross(a_coord, a_vel)
        # a_plane_normal_mag = vector_magnitude(a_plane_normal)
        # ang_i = math.degrees(math.acos(a_plane_normal[2]/a_plane_normal_mag))
        row = [
            x,
           a_coord[0], a_coord[1], a_coord[2],
           a_vel[0], a_vel[1], a_vel[2],
           -1,
           -1
        ]
        output.append(row)
    # Print
    print("Initial state found")
    max_seconds = 3600 * 24 * 365 * 5
    steps = 10000
    for t in range(0, max_seconds, steps):
        m_c = mars_coords(t)
        for i in range(num_asteroids):
            a_coord = [output[i][1], output[i][2], output[i][3]]
            a_vel = [output[i][4], output[i][5], output[i][6]]
            a_c = asteroid_coords(t, a_coord, a_vel)
            d = euclid_dist(m_c, a_c)
            if (output[i][DIST_COL_INDEX]<0) or (d<output[i][DIST_COL_INDEX]):
                output[i][DIST_COL_INDEX] = d
                output[i][TIME_COL_INDEX] = t
        print("Time", t, "/", max_seconds)
    # Print
    print("Calculation done")
    store_output(output)



def asteroid_coords(t, a_coord, a_vel):
    w = angular_velocity(a_coord, a_vel)
    a_coord[2] = 0
    theta_0 = math.atan(a_coord[1]/a_coord[0])
    a_r = vector_magnitude(a_coord)
    delta_theta = ((w * t) * 180 / math.pi) % 360
    final_theta = theta_0 + delta_theta
    x, y = a_r*cos(final_theta), a_r*sin(final_theta)
    return [x, y, 0]


def mars_coords(t):
    theta_0 = math.atan(HCC_MARS_AU[1]/HCC_MARS_AU[0])
    mars_r = vector_magnitude(au_to_km(HCC_MARS_AU))
    delta_theta = ((MARS_WO * t) * 180 / math.pi) % 360
    final_theta = theta_0 + delta_theta
    x, y = mars_r*cos(final_theta), mars_r*sin(final_theta)
    return [x, y, 0]


def angular_velocity(coord, vel):
    return vector_magnitude(vel) / vector_magnitude(coord)


def vector_magnitude(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])


def euclid_dist(p1, p2):
    return math.sqrt( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2 )


if __name__ == '__main__':
    main()
