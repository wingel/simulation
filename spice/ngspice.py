#! /usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys

import numpy as np
from subprocess import Popen, PIPE, STDOUT
from tempfile import mkstemp

from .simulator import SimulatorBase
from .rawfile import RawFile

class Ngspice(SimulatorBase):
    def __init__(self, trace = None):
        if not trace:
            trace = self.default_trace
        self.trace = trace

    def default_trace(self, s):
        self.output.append(s)

    def _simulate(self, circuit, pre, post):
        title = "simulation"

        self.output = []

        fd, raw_path = mkstemp(suffix = '.raw', prefix = 'spice')
        os.close(fd)

        fd, cir_path = mkstemp(suffix = '.cir', prefix = 'spice')
        with os.fdopen(fd, 'w') as f:
            f.write('%s\n' % title)
            f.write('%s\n' % pre)
            f.write('%s\n' % self.circuit_to_spice(circuit))
            f.write('%s\n' % post)
            f.write('.end\n')

        cmd = 'ngspice -b -r %s %s' % (raw_path, cir_path)
        self.trace(cmd + '\n')

        p = Popen(cmd, shell = True,
                  stdin = PIPE, stdout = PIPE, stderr = STDOUT,
                  close_fds = True)
        while 1:
            buf = p.stdout.readline()
            if not buf:
                break
            self.trace(buf)

        ec = p.wait()

        if ec != 0:
            print('\n'.join(self.output))
            return None

        with open(raw_path, 'rb') as f:
            rf = RawFile(f, '\n')
            data = rf.load()
            assert not rf.read(1)

        os.unlink(cir_path)
        os.unlink(raw_path)

        return data

    def _simulate_simple(self, circuit, *args):
        return self._simulate(circuit, '', ' '.join(
            [ self.fix_param(_) for _ in args ]))

    def dc(self, circuit, source, start, stop, step):
        args = [ '.dc', source, start, stop, step ]
        return self._simulate_simple(circuit, *args)

    def ac(self, circuit, variation, n, fstart, fstop):
        args = [ '.ac', variation, n, fstart, fstop ]
        return self._simulate_simple(circuit, *args)

    def tran(self, circuit, tstep, tstop, tstart=0, tmax=None, uic=False):
        args = [ '.tran', tstep, tstop, tstart ]
        if tmax is not None:
            args.append(tmax)
        if uic:
            args.append('uic')
        return self._simulate_simple(circuit, *args)

Simulator = Ngspice
