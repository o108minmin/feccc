#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from numpy import array


class DDarray:

    def __init__(self, high, low):
        self.high = high
        self.low = low

    @staticmethod
    def ddarray(high):
        low = np.zeros(high.size)
        low = low.reshape(high.shape)
        return DDarray(high, low)
