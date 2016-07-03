#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import float_info
import math
from math import ldexp
from math import isnan
from math import isinf
from math import fabs
from math import sqrt
from feccc.roundmode import roundmode
from numba.decorators import jit
from numba.types import float64
from numpy import nextafter
'''
# Calculate addition, subtraction, multiplication, division and root with rounding mode.

# using exsample
from pint import roundfloat as rf
from pint import roundmode as rdm

# Calculate 0.25 + 0.1 with rounding to up.
rf.rdadd(0.25, 0.1, rdm.up)

# Calculate 0.25 - 0.1 with rounding to down
rf.rdsub(0.25, 0.1, rdm.down)
'''


'''
constants

L = ldexp
M = minus
P = plus
LM969 = ldexp(1, -969)
'''
L27P1 = ldexp(1, 27) + 1
L28 = ldexp(1, 28)
LM28 = ldexp(1, -28)
L53 = ldexp(1, 53)
LM53 = ldexp(1, -53)
L105 = ldexp(1, 105)
LM105 = ldexp(1, -105)
L106 = ldexp(1, 106)
L537 = ldexp(1, 537)
L918 = ldexp(1, 918)
L996 = ldexp(1, 996)
LM969 = ldexp(1, -969)
LM1021 = ldexp(1, -1021)
L1023 = ldexp(1, 1023)
LM1023 = ldexp(1, -1023)
LM1074 = ldexp(1, -1074)
LM53PLM105 = (ldexp(1, -53) + ldexp(1, -105))

floatinf = float("inf")
floatmax = float_info.max

@jit
def split(a):
    tmp = a * (L27P1)
    x = tmp - (tmp - a)
    y = a - x
    return x, y

@jit([float64(float64)])
def succ(a):
    s = nextafter(a, 1)
    return s

@jit([float64(float64)])
def pred(a):
    r = nextafter(a, -1)
    return r

# by Masahide Kashiwagi
# http://verifiedby.me/adiary/029
@jit
def fasttwosum(a, b):
    x = a + b
    tmp = x - a
    y = b - tmp
    return x, y

@jit
def twosum_type1(a, b):
    x = a + b
    tmp = x - a
    y = (a - (x - tmp)) + (b - tmp)
    return x, y

@jit
def twosum_type2(a, b):
    x = a + b
    if fabs(a) > fabs(b):
        tmp = x - a
        y = b - tmp
    else:
        tmp = x - b
        y = a - tmp
    return x, y

# setting twosum type
twosum = twosum_type2

@jit
def twoproduct(a, b):
    arg1 = a
    arg2 = b
    x = arg1 * arg2
    if fabs(arg1) > L996:
        arg1fix = arg1 * LM28
        arg2fix = arg2 * L28
    elif fabs(arg2) > L996:
        arg1fix = arg1 * L28
        arg2fix = arg2 * LM28
    else:
        arg1fix = arg1
        arg2fix = arg2
    aH, aL = split(arg1fix)
    bH, bL = split(arg2fix)
    if fabs(x) > L1023:
        y = aL * bL - ((((x * 0.5) - (aH * 0.5) * bH) * 2. - aL * bH) - aH * bL)
    else:
        y = aL * bL - (((x - aH * bH) - aL * bH) - aH * bL)
    return x, y

@jit
def rdadd_up(a, b):
    x, y = twosum(a, b)
    if x == floatinf:
        return x
    elif x == -floatinf:
        if a == -floatinf or b == -floatinf:
            return x
        else:
            return -floatmax
    if y > 0:
        x = succ(x)
    return x

@jit
def rdadd_down(a, b):
    x, y = twosum(a, b)
    if x == floatinf:
        if a == floatinf or b == floatinf:
            return x
        else:
            return floatmax
    elif x == -floatinf:
        return x
    if y < 0:
        return pred(x)
    return x

def rdadd(a, b, rmode=roundmode.nearest):
    if rmode == roundmode.up:
        return rdadd_up(a, b)
    elif rmode == roundmode.down:
        return rdadd_down(a, b)
    elif rmode == roundmode.nearest:
        return a + b

def rdsub_up(a, b):
    return rdadd_up(a, -b)

def rdsub_down(a, b):
    return rdadd_down(a, -b)

def rdsub(a, b, rmode=roundmode.nearest):
    return rdadd(a, -b, rmode)

@jit
def rdmul_up(a, b):
    x, y = twoproduct(a, b)
    if x == floatinf:
        return x
    elif x == -floatinf:
        if fabs(a) == floatinf or fabs(b) == floatinf:
            return x
        else:
            return -floatmax
    if fabs(x) >= LM969:
        if y > 0:
            return succ(x)
    return x

@jit
def rdmul_down(a, b):
    x, y = twoproduct(a, b)
    if x == floatinf:
        if fabs(a) == floatinf or fabs(b) == floatinf:
            return x
        else:
            return floatmax
    elif x == -floatinf:
        return x
    if fabs(x) >= LM969:
        if y < 0.:
            return pred(x)
    else:
        s1, s2 = twoproduct(a * L537, b * L537)
        t = (x * L537) * L537
        if t > s1 or (t == s1 and s2 < 0.):
            return pred(x)
    return x

def rdmul(a, b, rmode=roundmode.nearest):
    if rmode == roundmode.up:
        return rdmul_up(a, b)
    elif rmode == roundmode.down:
        return rdmul_down(a, b)
    elif rmode == roundmode.nearest:
        return a * b

@jit
def rddiv_up(a, b):
    if a == 0. or b == 0.:
        return a / b
    if(fabs(a) == floatinf or fabs(b) == floatinf or isnan(a) or isnan(b)):
        return a / b
    if b < 0.:
        afix = -a
        bfix = -b
    else:
        afix = a
        bfix = b
    if fabs(afix) < LM969:
        if fabs(bfix) < L918:
            afix *= L105
            bfix *= L105
        else:
            if afix < 0.:
                return 0.
            else:
                return LM1074
    d = afix / bfix
    if d == floatinf:
        return d
    elif d == -floatinf:
        return -floatmax
    x, y = twoproduct(d, bfix)
    if x < afix or (x == afix and y < 0.):
        return succ(d)
    return d

@jit
def rddiv_down(a, b):
    if a == 0. or b == 0.:
        return a / b
    if fabs(a) == floatinf or fabs(b) == floatinf or isnan(a) or isnan(b):
        return a / b
    if b < 0.:
        afix = -a
        bfix = -b
    else:
        afix = a
        bfix = b
    if fabs(afix) < LM969:
        if fabs(bfix) < L918:
            afix *= L105
            bfix *= L105
        else:
            if afix < 0.:
                return -LM1074
            else:
                return 0
    d = afix / bfix
    if d == floatinf:
        return floatmax
    elif d == -floatinf:
        return d
    x, y = twoproduct(d, bfix)
    if x > afix or (x == afix and y > 0.):
        return pred(d)
    return d

def rddiv(a, b, rmode=roundmode.nearest):
    if rmode == roundmode.up:
        return rddiv_up(a, b)
    elif rmode == roundmode.down:
        return rddiv_down(a, b)
    elif rmode == roundmode.nearest:
        return a / b

@jit
def rdsqrt_up(a):
    d = sqrt(a)
    if a < LM969:
        a2 = a * L106
        d2 = d * L53
        x, y = twoproduct(d2, d2)
        if x < a2 or (x == a2 and y < 0.):
            d = succ(d)
    x, y = twoproduct(d, d)
    if x < a or (x == a and y < 0.):
        return succ(d)
    return d

@jit
def rdsqrt_down(a):
    d = sqrt(a)
    if a < LM969:
        a2 = a * L106
        d2 = d * L53
        x, y = twoproduct(d2, d2)
        if x > a2 or (x == a2 and y > 0.):
            d = pred(d)
    x, y = twoproduct(d, d)
    if x > a or (x == a and y > 0.):
        return pred(d)
    return d

def rdsqrt(a, rmode=roundmode.nearest):
    if rmode == roundmode.up:
        return rdsqrt_up(a)
    if rmode == roundmode.down:
        return rdsqrt_down(a)
    elif rmode == roundmode.nearest:
        return sqrt(a)
