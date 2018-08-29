#! /usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals

from spice.models import LibraryManager

if __name__ == '__main__':
    manager = LibraryManager(
        'models_source',
        'models_download',
        'models')
    manager.resolve()
    manager.process()
