#! /usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np

class _Unit(object):
    def __init__(self, multiplier, suffix, value = 1.0):
        assert isinstance(value, int) or isinstance(value, float)
        self.value = float(value) * multiplier
        self.multiplier = multiplier
        self.suffix = suffix

    def __rmul__(self, other):
        return self.__class__(self.multiplier, self.suffix, other)

    def __call__(self, value = 1):
        return self.__class__(self.multiplier, self.suffix, value)

    def __repr__(self):
        return str(self.value / self.multiplier) + self.suffix

    def __float__(self):
        return self.value

    def __int__(self):
        return int(self.value)

T = _Unit(1E12,  'T')
G = _Unit(1E9,   'G')
M = _Unit(1E6,   'M')
k = _Unit(1E3,   'k')
m = _Unit(1E-3,  'm')
u = _Unit(1E-6,  'u')
n = _Unit(1E-9,  'n')
p = _Unit(1E-12, 'p')
f = _Unit(1E-15, 'f')

_units = { _.suffix : _ for _ in [ T, G, M, k, m, u, n, p, f ] }

def parse_unit(s):
    u = _units.get(s[-1:])
    if u:
        return u(float(s[:-1]))
    return float(s)

def dBa(v):
    """Convert value to decibel for amplitudes"""
    return 20 * np.log10(np.abs(v))

def dBp(v):
    """Convert value to decibel for power"""
    return 10 * np.log10(np.abs(v))

def dBm(v):
    """Convert value to decibel for power * 1000

    This is usually used to display dB referenced to 1 mW"""
    return 20 * np.log10(np.abs(v) * 1000.0)

import unittest as _unittest

class _Test(_unittest.TestCase):
    def test_Units(self):
        self.assertEqual(k.value,            1.0E3)
        self.assertEqual(float(k),           1.0E3)
        self.assertEqual(int(k),             1000)
        self.assertEqual(float(k(3)),        3.0E3)
        self.assertEqual(float(3 * k),       3.0E3)
        self.assertEqual(repr(k),            '1.0k')
        self.assertEqual(repr(3 * k),        '3.0k')

        self.assertEqual(M.value,            1.0E6)
        self.assertEqual(int(M),             1000000)
        self.assertEqual(float(M),           1.0E6)
        self.assertEqual(float(M(3)),        3.0E6)
        self.assertEqual(float(3 * M),       3.0E6)
        self.assertEqual(repr(M),            '1.0M')
        self.assertEqual(repr(3 * M),        '3.0M')

if __name__ == '__main__':
    _unittest.main()
