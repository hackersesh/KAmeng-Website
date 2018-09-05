import math
import numpy as np

from constants import *
from utility import *


def get_asteroid_state(az, alt, r, vx, vy, vz):
    px, py, pz = altaz_to_tch(az, alt, r)
    gcec_coord = eq_to_ec(tch_to_gceq(px, py, pz))
    hcec_coord = gcec_to_hcec(gcec_coord)
    gcec_vel = eq_to_ec(tch_to_gceq(vx, vy, vz))
    hcec_vel = gcec_vel_to_hcec_vel(gcec_vel, gcec_coord)
    return hcec_coord, hcec_vel


def gcec_vel_to_hcec_vel(gcec_vel, gcec_coord):
    dist = np.array(HCC_EARTH_AU)
    wo = np.array([0, 0, EARTH_WO])
    wa = eq_to_ec(np.array([0, 0, EARTH_WA]))
    hcec_vel = gcec_vel + np.cross(dist, wo) + np.cross(wa, gcec_coord)
    return hcec_vel


def gcec_to_hcec(gceq_coord):
    obs_earth_coord = au_to_km(HCC_EARTH_AU)
    return np.add(obs_earth_coord, gceq_coord)


def tch_to_gceq(x, y, z):
    tch_to_gce = np.array([
        [-sin(K_THETA), -sin(K_FI)*cos(K_THETA), cos(K_FI)*cos(K_THETA)],
        [ cos(K_THETA), -sin(K_FI)*sin(K_THETA), cos(K_FI)*sin(K_THETA)],
        [          0,          cos(K_FI)   , sin(K_FI)]
    ])
    X = np.array([y, -x, z])
    gceq_coord = np.matmul(tch_to_gce, X)
    return gceq_coord


def altaz_to_tch(az, alt, r):
    x = -r * cos(alt) * cos(az)
    y = r * cos(alt) * sin(az)
    z = r * sin(alt)
    return x,y,z


def eq_to_ec(coord):
    m = np.array([
            [1, 0, 0],
            [0, cos(OB_EC), sin(OB_EC)],
            [0, -sin(OB_EC), cos(OB_EC)]
        ])
    return np.matmul(m, coord)


if __name__ == '__main__':
    # Test sample
    hcec_coord, hcec_vel = get_asteroid_state(
        192.8100706,32.42851414,191035815.3,
        -996.156284194396, -11280.2558612101, -2422.52905448753
    )
    print(hcec_coord)
    print(hcec_vel)
