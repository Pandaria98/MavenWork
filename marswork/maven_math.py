import math


def log(*args):
    print(*args)


def ln(num):
    # log(num)
    return math.log(num)


def temperatures_from_NGIMS(NGIMS, species):
    def init_values():
        i = 1
        alt0 = NGIMS['ALTITUDE'][i]
        n0 = NGIMS[density_key][i]
        r0 = (alt0 + R) * 1000

        i = 0
        alt = NGIMS['ALTITUDE'][i]
        n = NGIMS[density_key][i]
        r = (alt + R) * 1000

        num = -1 * G * M * m * (1 / r0 - 1 / r)
        den = (math.log(n) - math.log(n0)) * kB
        T = num / den
        log('init value', T)
        return T, n, r

    density_key = species + "_DENSITY"
    mole_weight = {
        'N2': 28,
    }
    G = 6.674e-11
    M = 6.4185e23
    R = 3389.5
    kB = 1.3806e-23

    coeff_relative_mole = 1.674e-27
    m = mole_weight[species] * coeff_relative_mole

    result = []
    T_prev, n_prev, r_prev = init_values()
    result.append(T_prev)
    for i in range(len(NGIMS)):
        alt = NGIMS['ALTITUDE'][i]
        n = NGIMS[density_key][i]
        r = (alt + R) * 1000

        lnT = ln(T_prev) - (ln(n) - ln(n_prev)) \
              - (G * M * m * (r - r_prev)) / (kB * T_prev * r_prev**2)
        T = math.e**lnT
        result.append(T)

        T_prev = T
        n_prev = n
        r_prev = r

    return result


def eddy_diffusion_from_NGIMS(self, species=['AR', 'N2']):
    pass
