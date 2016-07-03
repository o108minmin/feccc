#!/usr/bin/env python
# -*- coding: utf-8 -*-

from decimal import Decimal
from feccc import roundfloat as rf
from feccc.roundfloat import twosum, twoproduct


# TODO: Increase performance with numba


class DD:

    def __init__(self, high=0, low=0):
        self.high = high
        self.low = low

    def __str__(self):
        # high = Decimal(self.high)
        # low = Decimal(self.low)
        # return str(high + low)

        # debug mode
        return str(self.high) + " " + str(self.low)

    def __repr__(self):
        return str(self)


    def __pos__(self):
        return DD(self.high, self.low)

    def __neg__(self):
        return DD(-self.high, self.low)

    def __add__(self, arg):
        arg = DD.dd(arg)
        high, low = twosum(self.high, arg.high)
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

    def __mul__(self, a):
        pass

    def __truediv__(self, a):
        pass

    @staticmethod
    def dd(high=0, low=0):
        # TODO: Add string init
        if high.__class__.__name__ == 'DD':
            return DD(high.high, high.low)
        return DD(high, low)
