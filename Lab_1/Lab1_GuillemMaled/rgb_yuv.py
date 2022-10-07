import numpy as np


def rgb_2_yuv(r, g, b):
    """
    Args:
        r(int): red component. Take values from 0 to 255.
        g(int): green component. Take values from 0 to 255.
        b(int): blue component. Take values from 0 to 255.

    Returns:
        [y, u, v](array): return 3-value array with y, u, v components. Values from 0 to 255.
    """

    y = np.round(r * .299000 + g * .587000 + b * .114000, 1)
    u = np.round(r * -.168736 + g * -.331264 + b * .500000 + 128, 1)
    v = np.round(r * .500000 + g * -.418688 + b * -.081312 + 128, 1)

    return [y, u, v]


def yuv_2_rgb(y, u, v):
    """
     Args:
            y(int): y component. Take values from 0 to 255.
            u(int): u component. Take values from 0 to 255.
            v(int): v component. Take values from 0 to 255.

        Returns:
            [r, g, b](array): return 3-value array with r, g, b components. Values from 0 to 255.
        """

    r = np.round(y + 1.4075 * (v - 128), 1)
    g = np.round(y - 0.3455 * (u - 128) - (0.7169 * (v - 128)), 1)
    b = np.round(y + 1.7790 * (u - 128), 1)

    return [r, g, b]
