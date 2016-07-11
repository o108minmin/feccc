#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .roundmode import roundmode
from .ddbasic import DD
from .ddarray import DDarray
from feccc import ddbasicmath
from feccc import roundfloat
from feccc import floattool

dd = DD.dd
ddarray = DDarray.ddarray

__all__ = (
    'roundmode',
    'roundfloat',
    'floattool',
    'ddbasic',
    'ddbasicmath'
    'ddarray'
)
