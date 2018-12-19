import pydivide
import pandas
import numpy as np
from matplotlib import pyplot as plt

insitu = pydivide.read('2018-03-07', insitu_only=True)

orbit = insitu['Orbit']
io = insitu['IOflag']
sza = insitu['SPACECRAFT']['SZA']
h = insitu['SPACECRAFT']['ALTITUDE']


def select(all_data, instrument, orbit_num, h_min=120, h_max=240):
    df = all_data[instrument]
    j = 0
    p = pandas.DataFrame(
        index=np.hstack((df.columns.values,
                         np.array(['orbit', 'io', 'sza', 'h']))))
    for i in df.index.values:
        if orbit[i] == orbit_num and io[i] == "I":
            if h[i] >= h_min and h[i] <= h_max:
                p[j] = np.hstack((df.loc[i].values,
                                  np.array([orbit[i], io[i], sza[i], h[i]])))
                j += 1
    return p.T


NGIMS = select(insitu ,'NGIMS', 6680)
plt.plot(NGIMS['N2_DENSITY'], NGIMS['h'])
plt.show()
