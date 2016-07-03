#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
from math import fabs
from feccc import ddbasic
from numba.decorators import jit

# TODO: Increase performance with numba


def fabs(x):
    if x.high >= 0:
        return x
    else:
        return -x


def pow(x, y):
    if (y == 0):
        return dd(1.)
    a = y if y >= 0 else -y
    tmp = a
    r = ddbasic.DD.dd(1.)
    xp = x
    while (tmp != 0):
        if tmp % 2 != 0:
            r *= xp
        tmp //= 2
        xp = xp * xp
    if (y < 0):
        r = 1. / r
    return r


def ldexp(base, e):
    return base * pow(ddbasic.DD.dd(2.), e)
