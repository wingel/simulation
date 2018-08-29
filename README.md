# A Python library for simulation KiCad schematics using Spice

## Overview

This libray is at a very early stage of development.  There are
probably lots of bugs, and only Device:R, Device:C, Device:L and
Spice-enabled components have been tested so far.

## Example

[test-ngspice.py](test-ngspice.py) shows how to run a simulation using
Ngspice from the command line.

For a more adavanced example on how to use this library, see this
[Jupyter Notebook](butterworth.ipynb).  Just about anything in the
notebook can also be run directly from Python and produce output in an
interactive matplotlib window instead.

If you want to out the notebook yourself, follow the install
instructions below and then start the Jupyter notebook with:

```
jupyter notebook
```

If this doesn't work, try teling Jupyter not to start a browser and
then open the link that is printed in your preferred browser:

```
jupyter notebook --no-browser
```

## Prerequisites

I've been using the following libraries to run this:

* KiCad Version 5.0.0-rc2 nightly build as of 16 aug 2018
* Python 3.5 or Python 3.6 with pip
* Matplotlib 1.5.1 or 2.1.1
* Ngspice 26-1 or 27-1
* Jupyter Notebook =1.0.0

All this is running on Ubuntu 16.04 LTS or 18.04 LTS.

I don't see any reasons why this shouldn't work on other Linux
distributions or even on Windows, but I haven't tried it myself.

## The Xyce and LTspice simulation engines

There is also some support for the Xyce and LTspice engines.

I downloaded and installed the Xyce binaries for Ubuntu 16.04 (they
won't work on Ubuntu 18.04) from here:

> https://knowm.org/comparing-simulation-results-of-the-knowm-m-mss-model-in-xyce-and-jspice-using-qucs-s/

Note that the butterworth schematic will not work with Xyce as is.
For some reason the LMV981 OP-amp model causes a "timestamp too small"
error when trying to simulate the circuit.  Switching to a different
OP-amp model such as the LMH6624 does work though.

LTspiceXVII was installed using Wine on Ubuntu 16.04.

## Installation

Follow the instructions here on how to install the nightly build of
KiCad on Ubuntu:

> http://kicad-pcb.org/download/ubuntu/

Python, matplotlib and Ngspice, pip are the versionsions that come
with Ubunutu and can be installed with:

```
apt-get install python3 python3-pip python3-matplotlib ngspice
```

Jupyter notebook was installed using pip with:

```
python3 -m pip install jupyter
```

## LICENSING

### Main libraries

Unless otherwise specified all files are licensed under the following
terms:

    Copyright (C) 2018 Christer Weinigel <christer@weinigel.se>

    This library is free software; you can redistribute it and/or
    modify it under the terms of the GNU Lesser General Public
    License as published by the Free Software Foundation; either
    version 2.1 of the License, or (at your option) any later version.

    This library is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the [GNU
    Lesser General Public License](LICENSE.txt) for more details.

In plain english: If you use these libraries in your application, you
do not have to publish the source to your application.  But if you
make modifications to the spice or kicard libraries themselves you
have give publish those changes.

### Example code

You can use the source code in the Jupyter notebooks (*.ipynb) and
test applications (test-*.py) any way you like.  They are meant to be
used as examples and can be treated as public domain.  If your
jurisdiction will not recognise public domain, you can choose to treat
these files as licensed under the terms of the MIT License:

    Copyright (c) 2018 Christer Weinigel

    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use, copy,
    modify, merge, publish, distribute, sublicense, and/or sell copies
    of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.

### spice/patch.py

The file spice/patch.py was originally written by the user techtonik
on github and is available here:

    https://github.com/techtonik/python-patch

This file is licensed under the following terms:

    MIT License
    -----------

    Copyright (c) 2008-2016 anatoly techtonik

    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use, copy,
    modify, merge, publish, distribute, sublicense, and/or sell copies
    of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.

The file has since been modified slightly by Christer Weinigel to
allow for in patching of files in memory.

### Spice models

The vendor spice models found in models_source are copyrighted by the
respective vendors.  More information on licensing can be found in
each file.

As far as I know I am following all the license requirements for
distributing these files.  If I have inadvertly failed to do so and
you want me to remove a file, please send me a mail at
<christer@weinigel.se> and I will do so promptly.
