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
        # log('init value', T)
        return T, n, r

    density_key = species + "_DENSITY"
    mole_weight = {
        'N2': 28,
        'AR': 40,
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


def eddy_diffusion_from_NGIMS(NGIMS, species=('N2', 'AR')):
    mole_weight = {
        'N2': 28,
        'AR': 40,
    }
    G = 6.674e-11
    M = 6.4185e23
    R = 3389.5
    kB = 1.3806e-23

    # FIXME: assume T as constant
    # T = 150

    s0 = species[0]
    s1 = species[1]

    den0 = s0 + "_DENSITY"
    den1 = s1 + "_DENSITY"

    A = 18.8e16 if s0 == 'N2' else 22.3e16
    s = 0.82 if s0 == 'N2' else 0.75

    n_gradient = n_gradient_from_NGIMS(NGIMS, s1)
    T0_var = temperatures_from_NGIMS(NGIMS, s0)
    T1_var = temperatures_from_NGIMS(NGIMS, s1)

    D_result = []
    result = []
    for i in range(len(NGIMS) - 1):
        n0 = NGIMS[den0][i]
        n1 = NGIMS[den1][i]

        T0 = T0_var[i]
        H0 = kB * T0 / mole_weight[s0]
        T1 = T1_var[i]
        H1 = kB * T1 / mole_weight[s1]

        D10 = A * T1**s / n0
        K = D10 * ((1 / n1 * n_gradient[i]) + (1 / H1)) / ((1 / n1 * n_gradient[i]) + 1 / H0)

        D_result.append(D10)
        result.append(K)
    return D_result, result


def n_gradient_from_NGIMS(NGIMS, species):
    result = []

    density_key = species + '_DENSITY'
    # n_prev = NGIMS[density_key][-1]
    # r_prev = NGIMS['ALTITUDE'][-1] * 1e5
    n_prev = NGIMS[density_key][0]
    r_prev = NGIMS['ALTITUDE'][0] * 1e5
    for i in range(1, len(NGIMS)):
        n = NGIMS[density_key][i]
        r = NGIMS['ALTITUDE'][i] * 1e5

        gradient = (n - n_prev) / (r - r_prev)
        # result.insert(0, gradient)
        result.append(gradient)

        n_prev = n
        r_prev = r

    result.append(result[-1])
    return result


def reversed_range(num):
    return range(num - 1, -1, -1)
