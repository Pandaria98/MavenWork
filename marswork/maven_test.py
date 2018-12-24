import maven_data
import maven_math

from matplotlib import pyplot as plt


def log(*args):
    print(*args)


def test1():
    NGIMS = maven_data.data_from_pkl('../2018-03-07_NGIMS.pkl')
    Ts = maven_math.temperatures_from_NGIMS(NGIMS)

    log(Ts)
    plt.plot(Ts)
    plt.show()
