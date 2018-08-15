# A Python library for simulation KiCad schematics using Spice

## Overview

This libray is at a very early stage of development.  There are
probably lots of bugs, and only Device:R, Device:C, Device:L and
Spice-enabled components have been tested so far.

## Example

[test-ngspice.py](test-ngspice.py) shows how to run a simulation from
the command line.

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
* Python 3.6.5
* Matplotlib 2.1.1
* Ngspice 27-1
* Jupyter Notebook =1.0.0

All this is running on Ubuntu 18.04 LTS.

I don't see any reasons why this shouldn't work on other Linux
distributions or even on Windows, but I haven't tried it myself.

## Installation

Follow the instructions here on how to install the nightly build of
KiCad on Ubuntu:

> http://kicad-pcb.org/download/ubuntu/

Python, matplotlib and Ngspice are the versionsions that come with
Ubunutu and can be installed with:

```
apt-get install python3 python3-matplotlib ngspice
```

Jupyter notebook was installed using pip with:

```
python3 -m pip install jupyter
```

## LICENSE

Copyright (C) 2018 Christer Weinigel <christer@weinigel.se>

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the [GNU
Lesser General Public License](LICENSE.txt) for more details.
