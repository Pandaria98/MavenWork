import matplotlib.pyplot as plt
import cdflib


f = cdflib.CDF(r'..\data\maven.euv.modelled\data\minute\2017\01\mvn_euv_l3_minute_20170101_v11_r03.cdf')
y = f.varget('y')
v = f.varget('v')

plt.figure()
plt.title('EUV')
plt.xlabel('Wavelength')
plt.ylabel('Irradiance')
plt.plot(v[0], y[0])
plt.show()


def max_wave_length(y):
    for i, value in enumerate(y[0]):
        if value > 0.0025:
            print("max wave length: ", i)