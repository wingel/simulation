#! /usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import os
import hashlib

if sys.version_info.major < 3:
    STRING_TYPES = (str, unicode)
else:
    STRING_TYPES = str

_base_name = None
_models = {}

class Path(object):
    def __init__(self, url, hash = None, base = ''):
        i = url.find('://')
        if i != -1:
            scheme = url[:i]
            path = url[i+2:]
        else:
            scheme = None
            path = url.replace('\\', '/')

            if not path.startswith('/'):
                path = _base_name + '/' + path

        if 0:
            parts = path.split('/')
            for i in range(len(parts)-1, 0, -1):
                if parts[i].lower().endswith('.zip'):
                    basefile = ZipPath('/'.join(parts[:i]))
                    break

        self.scheme = scheme
        self.path = path
        self.hash = hash

    def load(self, base):
        path = os.path.join(base, self.path)
        text = normalize_text(open(path).read())
        calc = calculate_hash(text)

        print('%s: %s' % (path, calc))
        if self.hash and self.hash != calc:
            print("%s: hash mismatch, expected %s" % (path, self.hash))

        return text

    def __repr__(self):
        return 'Path(%s, %s)' % (repr(self.path), self.hash)

class Model(object):
    def __init__(self, name, mod, doc = None, base = ''):
        if not name.startswith('/'):
            name = _base_name + name
        if not base:
            base = _base_name
        if not base.endswith('/'):
            base += '/'

        self.name = name
        self.base = base
        self.mod = parse_spec(mod)
        self.doc = parse_spec(doc)

        assert name not in _models
        _models[name] = self

    def __repr__(self):
        return "Model: %s" % (self.name)

def normalize_text(text):
    text = '\n'.join([ _.rstrip() for _ in text.split('\n') ])
    text = text.replace('\r', '')
    return text

def calculate_hash(text):
    return hashlib.sha1(text).hexdigest().lower()[:20]

def parse_spec(spec):
    if spec is None:
        return None
    elif isinstance(spec, Path):
        return spec
    elif isinstance(spec, tuple):
        assert len(spec) == 2
        return Path(spec[0], spec[1].lower())
    else:
        return Path(spec)

class LibraryManager(object):
    def __init__(self, source_path, download_path, output_path):
        self.source_path = source_path
        self.download_path = download_path
        self.output_path = output_path
        self.mod_ext = '.lib'
        self.doc_ext = '.txt'

    def resolve(self):
        for root, dirs, files in os.walk(self.source_path):
            for fn in files:
                if os.path.normcase(fn) == 'models.py':
                    global _base_name
                    _base_name = os.path.relpath(root, self.source_path)
                    _base_name = _base_name.replace('\\', '/')
                    _base_name = _base_name + '/'
                    p = os.path.join(root, fn)
                    print("Processing", p)
                    l = {}
                    execfile(p, globals(), l)
                    if l:
                        print(l)
        print()

    def process(self):
        for name, model in sorted(_models.items()):
            src_base = os.path.join(self.source_path)
            dst_base = os.path.join(self.output_path, model.name)

            dst_dir = dst_base.rsplit('/', 1)[0]
            if not os.path.isdir(dst_dir):
                os.makedirs(dst_dir)

            text = model.mod.load(src_base)
            dst_path = dst_base + self.mod_ext
            tmp_path = dst_path + '+'
            open(tmp_path, 'w').write(text)
            os.rename(tmp_path, dst_path)

            if model.doc:
                text = model.doc.load(src_base)
                dst_path = dst_base + self.doc_ext
                tmp_path = dst_path + '+'
                open(tmp_path, 'w').write(text)
                os.rename(tmp_path, dst_path)

    print()

if __name__ == '__main__':
    manager = LibraryManager(
        '../models_source',
        '../models_download',
        '../models')
    manager.resolve()
    manager.process()

