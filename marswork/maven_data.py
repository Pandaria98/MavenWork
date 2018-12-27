import pickle
import pandas
import numpy as np


def log(*args):
    print(*args)


def data_from_pkl(pkl_path):
    with open(pkl_path, 'rb') as f:
        insitu = pickle.load(f)
    return insitu


def save_to_pkl(data, pkl_path):
    with open(pkl_path, 'wb') as f:
        pickle.dump(data, f)


def filtered_instrument_data(insitu, instrument, orbit=6680):
    instrument_data = insitu[instrument]
    append_extra_columns(insitu, instrument_data)
    instrument_data = filter_by_alt_inbound(instrument_data, orbit=orbit)
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


if __name__ == '__main__':
    insitu_path = '../2018-03-07.pkl'
    insitu = data_from_pkl(insitu_path)

    for orbit in range(6678, 6683):
        NGIMS = filtered_instrument_data(insitu, 'NGIMS', orbit=orbit)

        NGIMS_path = '../2018-03-07_NGIMS_{orbit}.pkl'.format(orbit=orbit)
        save_to_pkl(NGIMS, NGIMS_path)
