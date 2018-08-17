#! /usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys

import numpy as np
from subprocess import Popen, PIPE, STDOUT
import tempfile
import time
import shutil

from . import unit

class Dataset(dict):
    pass

class SimulatorBase(object):
    ENCODING = 'utf-8'
    SEPARATOR = '\n'
    BLOCKSIZE = 16
    BASE = '.'

    def __init__(self, trace = None):
        if not trace:
            trace = self._default_trace
        self.trace = trace
        self.timing = 1

    def _default_trace(self, s):
        self.output.append(s)

    def fix_param(self, v):
        if isinstance(v, unit._Unit):
            suffix = v.suffix
            if suffix == 'M':
                suffix = 'MEG'
            return str(v.value / v.multiplier) + suffix

        return str(v)

    def device_to_spice(self, device):
        a = []
        a.append(device.ref)
        for node in device.nodes:
            a.append(str(node))
        a.append(self.fix_param(device.value))
        for arg in device.args:
            a.append(self.fix_param(arg))
        for k, v in device.kwargs:
            a.append('%s=%s' % (k, self.fix_param(v)))
        return ' '.join(a)

    def circuit_to_spice(self, circuit, base = '.'):
        a = []

        for include in circuit.includes:
            a.append('.include %s' % os.path.join(base, include))
        for device in circuit.devices.values():
            a.append(self.device_to_spice(device))

        a.append('')

        return '\n'.join(a)

    def readline(self):
        while 1:
            i = self.buf.find(self.separator, self.offset)
            if i != -1:
                break

            data = self.f.read(self.BLOCKSIZE)
            if not data:
                return None

            # print("got %d bytes" % len(data))

            if self.offset:
                self.buf = self.buf[self.offset:]
                self.offset = 0

            self.buf += data

        s = self.buf[self.offset:i].decode(self.ENCODING)

        self.offset = i + len(self.separator)

        return s

    def readheader(self):
        l = self.readline()
        if l is None:
            return None, None
        i = l.find(':')
        return (l[:i], l[i+1:].strip())

    def read(self, n):
        while len(self.buf) < self.offset + n:
            data = self.f.read(max(self.BLOCKSIZE, n - len(self.buf) + self.offset))
            if not data:
                break

            # print("got %d bytes" % len(data))

            if self.offset:
                self.buf = self.buf[self.offset:]
                self.offset = 0

            self.buf += data

        data = self.buf[self.offset:self.offset + n]

        self.offset += n

        return data

    def _load(self, f):
        self.f = f

        self.buf = bytearray()
        self.offset = 0

        self.separator = bytearray(self.SEPARATOR, self.ENCODING)

        dataset = Dataset()

        k, v = self.readheader()
        assert k == 'Title'
        dataset.title = v

        k, v = self.readheader()
        assert k == 'Date'
        dataset.date = v

        k, v = self.readheader()
        assert k == 'Plotname'
        dataset.plotname = v

        k, v = self.readheader()
        assert k == 'Flags'
        dataset.flags = v.split()

        k, v = self.readheader()
        assert k == 'No. Variables'
        dataset.nr_variables = int(v)

        k, v = self.readheader()
        assert k == 'No. Points'
        dataset.nr_points = int(v)

        while 1:
            k, v = self.readheader()
            if k == 'Variables':
                break
            print("Extra header: %s: %s" % (k, v))
        assert k == 'Variables'
        assert not v

        dataset.unit = {}
        dataset.params = {}

        self.variables = []
        for idx in range(dataset.nr_variables):
            parts = self.readline().strip().split()
            assert int(parts[0]) == idx
            name = parts[1]
            unit = parts[2]
            params = {}
            for s in parts[3:]:
                i = s.find('=')
                params[s[:i]] = s[i+1:]
            self.variables.append((name, unit, params))

        k, v = self.readheader()
        assert k == 'Binary'
        assert not v

        self.update_variables(dataset)

        # Doing str here is a workaround for numpy 1.11 not understanding unicode
        dt = np.dtype([ (str(name), type) for (name, type) in dataset.dt ])

        n = dataset.nr_points * dt.itemsize
        buf = self.read(n)
        # print(n, len(buf))

        data = np.frombuffer(buf, dtype = dt, count = dataset.nr_points)

        for k in dataset.unit.keys():
            dataset[k] = data[str(k)]

        return dataset

    def _make_cmd(self, cir_path, raw_path):
        return '%s -b -r %s %s' % (self.SIMULATOR, raw_path, cir_path)

    def _write_circuit(self, fn, circuit, pre, post):
        title = "simulation"

        with open(fn, 'w') as f:
            cir = self.circuit_to_spice(circuit, base = self.BASE)
            f.write('%s\n' % title)
            f.write('%s\n' % pre)
            f.write('%s\n' % cir)
            f.write('%s\n' % post)
            f.write('.end\n')
            f.close()

    def _simulate(self, circuit, pre, post):
        self.output = []

        base = tempfile.mkdtemp(prefix = 'sim-', dir = '.')

        cir_path = os.path.join(base, 'spice.cir')
        raw_path = os.path.join(base, 'spice.raw')

        self._write_circuit(cir_path, circuit, pre, post)

        cmd = self._make_cmd(cir_path, raw_path)
        print(cmd)
        self.trace(cmd + '\n')

        t0 = time.time()
        p = Popen(cmd, shell = True,
                  stdin = PIPE, stdout = PIPE, stderr = STDOUT,
                  close_fds = True)
        while 1:
            buf = p.stdout.readline()
            if not buf:
                break
            self.trace(buf.decode('ascii'))
        ec = p.wait()
        t1 = time.time()

        if self.timing:
            print("simulation took %.3f seconds" % (t1-t0))

        if ec != 0:
            for l in self.output:
                sys.stdout.write(l)
            return None

        with open(raw_path, 'rb') as f:
            data = self._load(f)
            assert len(self.read(1)) == 0

        shutil.rmtree(base)

        return data

    def _fixup_data(self, data):
        return data

    def _simulate_simple(self, circuit, *args):
        args = [ self.fix_param(_) for _ in args ]
        return self._simulate(circuit, '', ' '.join(args))

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
