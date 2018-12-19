import pydivide
import pandas
import numpy as np
import math

from matplotlib import pyplot as plt


def ln(num):
    return math.log(num)


def my_data(insitu):
    NGIMS = insitu['NGIMS']
    append_extra_columns(insitu, NGIMS)
    NGIMS = filter_by_alt_inbound(NGIMS)
    return NGIMS


def append_extra_columns(insitu, instrument_data):
    data = instrument_data

    orbit = insitu['Orbit']
    io = insitu['IOflag']
    sza = insitu['SPACECRAFT']['SZA']
    h = insitu['SPACECRAFT']['ALTITUDE']

    data['ORBIT'] = orbit
    data['IO_FLAG'] = io
    data['SZA'] = sza
    data['ALTITUDE'] = h


def isnt_nan(num):
    return not np.isnan(num)


def filter_by_alt_inbound(instrument_data):
    data = instrument_data
    data = data[data['ALTITUDE'] >= 120]
    data = data[data['ALTITUDE'] <= 240]
    data = data[data['ORBIT'] == 6680]
    data = data[data['IO_FLAG'] == 'I']

    data = data[pandas.notnull(data['N2_DENSITY'])]
    return data


def temperatures_from_data(NGIMS):
    def init_values():
        i = -1
        alt0 = NGIMS['ALTITUDE'][i]
        n0 = NGIMS['N2_DENSITY'][i]
        r0 = (alt0 + R) * 1000

        i = -20
        alt = NGIMS['ALTITUDE'][i]
        n = NGIMS['N2_DENSITY'][i]
        r = (alt + R) * 1000

        num = -1 * G * M * m * (1 / r0 - 1 / r)
        den = (math.log(n) - math.log(n0)) * kB
        T = num / den
        return T, n, r

    def reversed_idx():
        return range(len(NGIMS) - 1, -1, -1)

    mole_weight = {
        'N2': 28,
    }
    G = 6.674e-11
    M = 6.4185e23
    R = 3389.5
    kB = 1.3806e-23

    coeff_relative_mole = 1.674e-27
    m = mole_weight['N2'] * coeff_relative_mole

    result = []
    T_prev, n_prev, r_prev = init_values()
    result.append(T_prev)
    for i in reversed_idx():
        alt = NGIMS['ALTITUDE'][i]
        n = NGIMS['N2_DENSITY'][i]
        r = (alt + R) * 1000

        lnT = ln(T_prev) - (ln(n) - ln(n_prev)) \
              - (G * M * m * (r - r_prev)) / (kB * T_prev * r_prev**2)
        T = math.e**lnT
        result.append(T)

        T_prev = T
        n_prev = n
        r_prev = r

    return result
