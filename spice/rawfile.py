#! /usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np

class Dataset(dict):
    pass

class RawFile(object):
    def __init__(self, f, separator = '\n', blocksize = 16):
        self.f = f
        self.separator = bytearray(separator, 'ascii')
        self.blocksize = blocksize
        self.buf = bytearray()
        self.offset = 0

    def readline(self):
        while 1:
            i = self.buf.find(self.separator, self.offset)
            if i != -1:
                break

            data = self.f.read(self.blocksize)
            if not data:
                return None

            # print("got %d bytes" % len(data))

            if self.offset:
                self.buf = self.buf[self.offset:]
                self.offset = 0

            self.buf += data

        s = self.buf[self.offset:i].decode('ascii')

        self.offset = i + 1
        return s

    def readheader(self):
        l = self.readline()
        if l is None:
            return None, None
        i = l.find(':')
        return (l[:i], l[i+1:].strip())

    def read(self, n):
        while len(self.buf) < self.offset + n:
            data = self.f.read(max(self.blocksize, n - len(self.buf) + self.offset))
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

    def load(self):
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

        k, v = self.readheader()
        assert k == 'Variables'
        assert not v

        idxs = {}
        dataset.unit = {}
        dataset.params = {}
        for idx in range(dataset.nr_variables):
            parts = self.readline().strip().split()
            assert int(parts[0]) == idx
            name = parts[1]
            unit = parts[2]
            params = {}
            for s in parts[3:]:
                i = s.find('=')
                params[s[:i]] = s[i+1:]

            idxs[name] = idx
            dataset.unit[name] = unit
            dataset.params[name] = params

        k, v = self.readheader()
        assert k == 'Binary'
        assert not v

        n = dataset.nr_variables * dataset.nr_points
        if 'complex' in dataset.flags:
            buf = self.read(n * 8 * 2)
            a = np.frombuffer(buf, dtype = np.complex128, count = n)
        else:
            buf = self.read(n * 8)
            a = np.frombuffer(buf, dtype = np.float64, count = n)

        data = a.reshape((dataset.nr_variables, dataset.nr_points), order='F')

        for k, v in idxs.items():
            dataset[k] = data[v]

        return dataset
