#!/usr/bin/env python
# -*- coding: utf-8 -*-

from decimal import Decimal
from feccc.roundfloat import twosum, twoproduct
from math import isinf
from feccc import ddbasicmath as ddmath

# TODO: Debug for some numbers (inf, 0...)
# TODO: Increase performance with numba


class DD:

    def __init__(self, high=0, low=0):
        self.high = high
        self.low = low

    @staticmethod
    def dd(high=0, low=0):
        # TODO: Add string init
        if high.__class__.__name__ == 'DD':
            return DD(high.high, high.low)
        return DD(high, low)

    def __str__(self):
        # high = Decimal(self.high)
        # low = Decimal(self.low)
        # return str(high + low)

        # debug mode
        return str(self.high) + ' ' + str(self.low)

    def __repr__(self):
        return str(self)

    def __pos__(self):
        return DD(self.high, self.low)

    def __neg__(self):
        return DD(-self.high, self.low)

    def __add__(self, arg):
        arg = DD.dd(arg)
        high, low = twosum(self.high, arg.high)
        if isinf(high):
            return DD(high)
        low += self.low + arg.low
        high, low = twosum(high, low)
        return DD(high, low)

    def __radd__(self, arg):
        return DD.__add__(self, arg)

    def __iadd__(self, arg):
        return DD.__add__(self, arg)

    def __sub__(self, arg):
        return DD.__add__(self, -arg)

    def __rsub__(self, arg):
        return DD.__add__(-self, arg)

    def __isub__(self, arg):
        return DD.__add__(self, -arg)

    def __mul__(self, arg):
        arg = DD.dd(arg)
        high, low = twoproduct(self.high, arg.high)
        if isinf(high):
            return DD(high)
        low += self.high * arg.low + self.low * arg.high + self.low * arg.low
        high, low = twosum(high, low)
        return DD(high, low)

    def __rmul__(self, arg):
        return DD.__mul__(self, arg)

    def __imul__(self, arg):
        return DD.__mul__(self, arg)

    def __truediv__(self, arg):
        arg = DD.dd(arg)
        high = self.high / arg.high
        if isinf(high):
            return DD(high)
        if isinf(arg.high):
            return DD(high)
        h2, l2 = twoproduct(-high, arg.high)
        if isinf(h2):
            h2, l2 = twoproduct(-high, arg.high * 0.5)
            low = ((((h2 + (self.high * 0.5)) - high * (arg.low * 0.5)
                     ) + (self.low * 0.5)) + l2) / (arg.high * 0.5)
        else:
            low = ((((h2 + self.high) - high * arg.low) + self.low) + l2) / arg.high
        h2, l2 = twosum(high, low)
        return DD.dd(h2, l2)

    def __rtruediv__(self, arg):
        arg = DD.dd(arg)
        return DD.__truediv__(arg, self)

    def __itruediv__(self, arg):
        return DD.__truediv__(self, arg)

    def abs(self):
        return ddmath.fabs(self)
