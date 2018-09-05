import numpy as np
from constants import *


def au_to_km(a):
    return [x * AU_TO_KM for x in a]


def sin(a):
    return np.sin(np.deg2rad(a))


def cos(a):
    return np.cos(np.deg2rad(a))
