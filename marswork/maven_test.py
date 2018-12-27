import maven_data
import maven_math

from matplotlib import pyplot as plt


def log(*args):
    print(*args)


def test1():
    orbit = 6682
    NGIMS_path = '../2018-03-07_NGIMS_{orbit}.pkl'.format(orbit=orbit)
    NGIMS = maven_data.data_from_pkl(NGIMS_path)
    # Ts = maven_math.temperatures_from_NGIMS(NGIMS, 'N2')
    D, K = maven_math.eddy_diffusion_from_NGIMS(NGIMS)

    plt.plot(D)
    plt.plot(K)
    plt.show()


def test2():
    orbit = 6682
    NGIMS_path = '../2018-03-07_NGIMS_{orbit}.pkl'.format(orbit=orbit)
    NGIMS = maven_data.data_from_pkl(NGIMS_path)
    T = maven_math.temperatures_from_NGIMS(NGIMS, species='N2')

    plt.plot(T)
    plt.show()


if __name__ == '__main__':
    # test1()
    test2()
