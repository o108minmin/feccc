#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
from math import fabs


def fabs(x):
    if x.high >= 0:
        return x
    else:
        return -x
