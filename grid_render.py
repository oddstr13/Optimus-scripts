#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © Odd Stråbø <oddstr13@openshell.no> 2017
# License: MIT - https://opensource.org/licenses/MIT
#
import sys
sys.path.append("discord")
import gridrender

from PIL import Image


with open("delta.grid", "rb") as fh:
    im = gridrender.render(fh.read())

#print(im.palette)

im.save("output.png")
from PIL import Image

#im.putpalette(palette)
#im = Image.frombytes(mode='L', data=b'abcd', size=(2,2))
im.show()


#gridrender.renderPalette(gridrender.palette).resize((8,256)).show()