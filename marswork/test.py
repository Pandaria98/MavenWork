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


def draw_at(x, y):
    offset = x + y * 32
    offset += 65024
    memory[offset] = 195


def draw_column(x, y, column, column_num):
    i = 0
    while i < 8:
        should_draw = 1 & column
        if should_draw:
            real_x = x + column_num
            real_y = y + i
            draw_at(real_x, real_y)

        column >>= 1
        i += 1


def draw_char(text_code, x, y):
    text_address = 64512 + text_code * 4
    i = 0
    while i < 4:
        current_column = memory[text_address + i]
        draw_column(x, y, current_column, i)
        i += 1