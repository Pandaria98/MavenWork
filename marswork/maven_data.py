import pickle
import pandas
import numpy as np



def log(*args):
    print(*args)


def data_from_pkl(pkl_path):
    with open(pkl_path, 'rb') as f:
        insitu = pickle.load(f)
    return insitu


def filtered_instrument_data(insitu, instrument):
    instrument_data = insitu[instrument]
    append_extra_columns(insitu, instrument_data)
    instrument_data = filter_by_alt_inbound(instrument_data)
    return instrument_data


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


def filter_by_alt_inbound(instrument_data, alt_limit=(120, 240), orbit=6680):
    data = instrument_data

    low, high = alt_limit
    data = data[data['ALTITUDE'] >= low]
    data = data[data['ALTITUDE'] <= high]

    data = data[data['ORBIT'] == orbit]
    data = data[data['IO_FLAG'] == 'I']

    data = data[pandas.notnull(data['N2_DENSITY'])]
    return data
