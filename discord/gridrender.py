#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © Odd Stråbø <oddstr13@openshell.no> 2017
# License: MIT - https://opensource.org/licenses/MIT
#

import struct
import math

from PIL import Image, ImagePalette, ImageColor, ImageDraw

#palette_r = ['#ffffff','#fffffc','#fffff9','#fffff6','#fffff3','#fffff0','#ffffed','#ffffea','#ffffe7','#ffffe4','#ffffe1','#ffffde','#ffffdb','#ffffd8','#ffffd5','#ffffd2','#ffffcf','#ffffcc','#ffffc9','#ffffc6','#ffffc2','#ffffbf','#ffffbc','#ffffb9','#ffffb6','#ffffb3','#ffffb0','#ffffad','#ffffaa','#ffffa7','#ffffa3','#ffffa0','#ffff9d','#ffff9a','#ffff97','#ffff93','#ffff90','#ffff8d','#ffff8a','#ffff86','#ffff83','#ffff80','#ffff7c','#ffff79','#ffff75','#ffff72','#ffff6e','#ffff6a','#ffff67','#ffff63','#ffff5f','#ffff5b','#ffff57','#ffff52','#ffff4e','#ffff49','#ffff45','#ffff3f','#ffff3a','#ffff34','#ffff2d','#ffff26','#ffff1d','#ffff10','#fffe00','#fffb00','#fff900','#fff600','#fff300','#fff000','#ffed00','#ffea00','#ffe700','#ffe500','#ffe200','#ffdf00','#ffdc00','#ffd900','#ffd600','#ffd300','#ffd000','#ffcd00','#ffcb00','#ffc800','#ffc500','#ffc200','#ffbf00','#ffbc00','#ffb900','#ffb600','#ffb300','#ffb000','#ffad00','#ffaa00','#ffa700','#ffa300','#ffa000','#ff9d00','#ff9a00','#ff9700','#ff9400','#ff9000','#ff8d00','#ff8a00','#ff8600','#ff8300','#ff8000','#ff7c00','#ff7900','#ff7500','#ff7100','#ff6e00','#ff6a00','#ff6600','#ff6200','#ff5e00','#ff5a00','#ff5500','#ff5100','#ff4c00','#ff4700','#ff4200','#ff3c00','#ff3600','#ff2e00','#ff2600','#ff1c00','#ff0c00','#fe0005','#fd000f','#fc0016','#fa001c','#f90021','#f80026','#f6002b','#f5002f','#f30033','#f20037','#f0003b','#ef003f','#ed0043','#ec0047','#ea004a','#e9004e','#e70052','#e50055','#e40059','#e2005c','#e00060','#de0064','#dd0067','#db006b','#d9006e','#d70072','#d50075','#d30079','#d1007c','#cf0080','#cd0084','#ca0087','#c8008b','#c6008e','#c30092','#c10096','#be0099','#bc009d','#b900a0','#b600a4','#b300a8','#b000ab','#ad00af','#aa00b3','#a600b6','#a300ba','#9f00be','#9c00c1','#9800c5','#9300c9','#8f00cd','#8a00d0','#8500d4','#8000d8','#7b00dc','#7500df','#6e00e3','#6700e7','#5f00eb','#5600ef','#4c00f2','#3f00f6','#2f00fa','#1100fe','#0401fc','#0902f7','#0e03f3','#1105ee','#1406ea','#1607e5','#1808e1','#1a09dc','#1c0ad8','#1d0ad4','#1e0bcf','#1f0ccb','#200dc7','#210dc2','#220ebe','#230eba','#230eb5','#240fb1','#240fad','#2410a9','#2510a5','#2510a1','#25109c','#251098','#251194','#251190','#25118c','#251188','#251184','#251180','#25117c','#241178','#241174','#241170','#23116c','#231168','#221165','#221161','#21115d','#211059','#201056','#201052','#1f104e','#1e104b','#1d1047','#1d0f43','#1c0f40','#1b0f3c','#1a0e39','#190e35','#190d32','#180d2e','#170c2b','#160b28','#160a25','#140821','#13071e','#11061b','#0f0518','#0c0415','#090311','#06020c','#030106','#000000']
# http://gka.github.io/palettes/#colors=#fff,#0f0,#f00,#00f,#000|steps=256|bez=0|coL=0
#palette_r = ['#ffffff','#fdfffc','#fbfff9','#f8fff6','#f6fff2','#f4ffef','#f2ffec','#f0ffe9','#edffe6','#ebffe3','#e9ffe0','#e6ffdd','#e4ffd9','#e2ffd6','#dfffd3','#ddffd0','#daffcd','#d8ffca','#d6ffc7','#d3ffc3','#d1ffc0','#ceffbd','#ccffba','#c9ffb7','#c6ffb4','#c4ffb1','#c1ffad','#bfffaa','#bcffa7','#b9ffa4','#b6ffa1','#b4ff9d','#b1ff9a','#aeff97','#abff94','#a8ff90','#a5ff8d','#a2ff8a','#9fff86','#9cff83','#99ff80','#95ff7c','#92ff79','#8eff75','#8bff72','#87ff6e','#84ff6a','#80ff67','#7cff63','#78ff5f','#74ff5b','#70ff57','#6bff53','#67ff4f','#62ff4b','#5dff46','#57ff41','#51ff3c','#4bff37','#44ff31','#3cff2b','#33ff24','#28ff1b','#18ff0e','#10fe00','#2dfc00','#3df900','#4af700','#54f500','#5df200','#64f000','#6bed00','#72ea00','#78e800','#7de500','#83e300','#88e000','#8cde00','#91db00','#95d900','#99d600','#9dd300','#a1d100','#a4ce00','#a8cb00','#abc900','#aec600','#b1c300','#b4c100','#b7be00','#babb00','#bdb800','#bfb500','#c2b300','#c5b000','#c7ad00','#c9aa00','#cca700','#cea400','#d0a100','#d29e00','#d59b00','#d79800','#d99400','#db9100','#dd8e00','#de8b00','#e08700','#e28400','#e48000','#e67c00','#e77900','#e97500','#eb7100','#ec6d00','#ee6900','#ef6400','#f16000','#f25b00','#f45600','#f55000','#f74b00','#f84500','#f93e00','#fb3600','#fc2d00','#fd2100','#fe1000','#fe0005','#fd000f','#fc0016','#fa001c','#f90021','#f80026','#f6002b','#f5002f','#f30033','#f20037','#f0003b','#ef003f','#ed0043','#ec0047','#ea004a','#e9004e','#e70052','#e50055','#e40059','#e2005c','#e00060','#de0064','#dd0067','#db006b','#d9006e','#d70072','#d50075','#d30079','#d1007c','#cf0080','#cd0084','#ca0087','#c8008b','#c6008e','#c30092','#c10096','#be0099','#bc009d','#b900a0','#b600a4','#b300a8','#b000ab','#ad00af','#aa00b3','#a600b6','#a300ba','#9f00be','#9c00c1','#9800c5','#9300c9','#8f00cd','#8a00d0','#8500d4','#8000d8','#7b00dc','#7500df','#6e00e3','#6700e7','#5f00eb','#5600ef','#4c00f2','#3f00f6','#2f00fa','#1100fe','#0401fc','#0902f7','#0e03f3','#1105ee','#1406ea','#1607e5','#1808e1','#1a09dc','#1c0ad8','#1d0ad4','#1e0bcf','#1f0ccb','#200dc7','#210dc2','#220ebe','#230eba','#230eb5','#240fb1','#240fad','#2410a9','#2510a5','#2510a1','#25109c','#251098','#251194','#251190','#25118c','#251188','#251184','#251180','#25117c','#241178','#241174','#241170','#23116c','#231168','#221165','#221161','#21115d','#211059','#201056','#201052','#1f104e','#1e104b','#1d1047','#1d0f43','#1c0f40','#1b0f3c','#1a0e39','#190e35','#190d32','#180d2e','#170c2b','#160b28','#160a25','#140821','#13071e','#11061b','#0f0518','#0c0415','#090311','#06020c','#030106','#000000']
# http://gka.github.io/palettes/#colors=#fff,#0f0,#f00,#00f,#000|steps=256|bez=0|coL=1

#_palette_r = ['#ffffff','#fcfffa','#f8fff4','#f4ffef','#f0ffea','#ecffe5','#e9ffe0','#e4ffda','#e0ffd4','#dcffce','#d7ffc9','#d2ffc3','#ceffbd','#c9ffb7','#c4ffb1','#bfffab','#baffa4','#b5ff9e','#afff98','#a9ff91','#a2ff8a','#9cff83','#94ff7b','#8dff74','#85ff6c','#7dff63','#73ff5a','#68ff51','#5cff45','#4dff39','#39ff29','#19ff0f','#1efd00','#31fb00','#3cfa00','#42f800','#4cf600','#54f500','#57f400','#5ef100','#64f000','#6aee00','#6fec00','#74e900','#77e800','#7be700','#7fe500','#83e300','#87e100','#89df00','#8ddd00','#91db00','#95d800','#97d700','#9ad600','#9dd300','#a0d200','#a2d000','#a5ce00','#a8cb00','#aac900','#acc800','#afc600','#b0c500','#b3c200','#b5bf00','#b7be00','#b9bc00','#bbba00','#beb800','#bfb600','#c1b300','#c2b200','#c5b000','#c6ae00','#c8ab00','#caa900','#cba800','#cda600','#cfa200','#d0a100','#d29e00','#d49c00','#d59a00','#d79700','#d89600','#da9200','#db9000','#dc8e00','#de8c00','#df8900','#e08700','#e28500','#e38200','#e57e00','#e67c00','#e77900','#e87700','#e97500','#eb7100','#ec6e00','#ed6c00','#ed6900','#ef6500','#f06200','#f15e00','#f25b00','#f35700','#f45400','#f55000','#f64c00','#f74700','#f84300','#f93e00','#fa3800','#fb3200','#fc2c00','#fd2300','#fe1800','#ff0400','#fe000b','#fb0017','#f9001f','#f70028','#f50030','#f30035','#f0003b','#ef0040','#eb0047','#ea004c','#e70052','#e40057','#e2005b','#e00061','#de0065','#db006b','#d9006f','#d60074','#d3007a','#d0007d','#cd0084','#ca0088','#c6008d','#c40091','#c00096','#be0099','#bb009e','#b700a2','#b400a6','#b100ab','#ad00b0','#a900b4','#a600b7','#a200bb','#9d00c0','#9a00c3','#9600c6','#9100cb','#8d00cf','#8800d2','#8300d6','#7e00d9','#7700de','#7300e1','#6c00e4','#6700e7','#6000ea','#5a00ed','#5100f1','#4800f4','#3c00f7','#3000fa','#1b00fd','#0200fe','#0501fa','#0a02f7','#0d03f4','#1004f0','#1205ec','#1406e9','#1607e6','#1808e2','#1908de','#1a09db','#1c0ad8','#1d0ad5','#1e0bd1','#1f0ccd','#1f0cca','#200cc8','#210dc4','#210dc0','#220ebd','#230eba','#230eb7','#230fb3','#240fb0','#240fad','#240faa','#2510a5','#2510a2','#2510a0','#25109d','#25109a','#251196','#251192','#25118f','#25118d','#25118a','#251187','#251184','#251181','#25117d','#24117a','#241177','#241174','#241170','#24116e','#23116b','#231167','#231165','#221161','#22115e','#21115c','#211059','#211057','#201054','#201051','#1f104e','#1e104b','#1e1047','#1d0f47','#1d0f43','#1c0f40','#1b0f3d','#1b0f3a','#1a0e38','#190e36','#190e32','#180d30','#180c2d','#170c2a','#160b28','#160a25','#150924','#150821','#13081f','#12061c','#100519','#0e0516','#0c0414','#0a0312','#08030e','#050209','#020104','#000000']

# http://gka.github.io/palettes/#colors=#f00,#fff,#00f|steps=256|bez=0|coL=0
# Red - White - Blue
_palette_r = ['#ff0000','#ff0b03','#ff1406','#ff1a09','#ff1f0c','#ff240f','#ff2812','#ff2c15','#ff2f17','#ff3319','#ff361c','#ff391e','#ff3c20','#ff3e22','#ff4124','#ff4326','#ff4628','#ff482a','#ff4b2c','#ff4d2e','#ff4f30','#ff5232','#ff5434','#ff5636','#ff5838','#ff5a39','#ff5c3b','#ff5e3d','#ff603f','#ff6241','#ff6443','#ff6645','#ff6846','#ff6a48','#ff6c4a','#ff6d4c','#ff6f4e','#ff7150','#ff7351','#ff7553','#ff7655','#ff7857','#ff7a59','#ff7c5b','#ff7d5c','#ff7f5e','#ff8160','#ff8262','#ff8464','#ff8666','#ff8868','#ff8969','#ff8b6b','#ff8d6d','#ff8e6f','#ff9071','#ff9173','#ff9375','#ff9576','#ff9678','#ff987a','#ff9a7c','#ff9b7e','#ff9d80','#ff9e82','#ffa084','#ffa285','#ffa387','#ffa589','#ffa68b','#ffa88d','#ffa98f','#ffab91','#ffac93','#ffae95','#ffb097','#ffb199','#ffb39a','#ffb49c','#ffb69e','#ffb7a0','#ffb9a2','#ffbaa4','#ffbca6','#ffbda8','#ffbfaa','#ffc1ac','#ffc2ae','#ffc4b0','#ffc5b2','#ffc7b4','#ffc8b6','#ffcab8','#ffcbba','#ffcdbb','#ffcebd','#ffd0bf','#ffd1c1','#ffd3c3','#ffd4c5','#ffd6c7','#ffd7c9','#ffd9cb','#ffdacd','#ffdccf','#ffddd1','#ffdfd3','#ffe0d5','#ffe2d7','#ffe3d9','#ffe5db','#ffe6dd','#ffe8df','#ffe9e1','#ffebe3','#ffece5','#ffeee7','#ffefea','#fff1ec','#fff2ee','#fff4f0','#fff5f2','#fff7f4','#fff8f6','#fffaf8','#fffbfa','#fffdfc','#fffefe','#fefeff','#fdfcff','#fcfaff','#fbf9ff','#faf7ff','#f9f5ff','#f8f3ff','#f7f1ff','#f6efff','#f5edff','#f4ecff','#f3eaff','#f2e8ff','#f1e6ff','#f0e4ff','#efe2ff','#ede1ff','#ecdfff','#ebddff','#eadbff','#e9d9ff','#e8d7ff','#e7d6ff','#e6d4ff','#e5d2ff','#e3d0ff','#e2ceff','#e1ccff','#e0cbff','#dfc9ff','#dec7ff','#dcc5ff','#dbc3ff','#dac2ff','#d9c0ff','#d8beff','#d6bcff','#d5baff','#d4b8ff','#d3b7ff','#d2b5ff','#d0b3ff','#cfb1ff','#ceafff','#cdaeff','#cbacff','#caaaff','#c9a8ff','#c8a6ff','#c6a5ff','#c5a3ff','#c4a1ff','#c29fff','#c19eff','#c09cff','#be9aff','#bd98ff','#bc96ff','#ba95ff','#b993ff','#b791ff','#b68fff','#b58dff','#b38cff','#b28aff','#b088ff','#af86ff','#ad84ff','#ac83ff','#aa81ff','#a97fff','#a77dff','#a67cff','#a47aff','#a378ff','#a176ff','#a074ff','#9e73ff','#9d71ff','#9b6fff','#996dff','#986bff','#966aff','#9468ff','#9366ff','#9164ff','#8f62ff','#8d60ff','#8c5fff','#8a5dff','#885bff','#8659ff','#8457ff','#8255ff','#8054ff','#7e52ff','#7c50ff','#7a4eff','#784cff','#764aff','#7448ff','#7246ff','#7044ff','#6d42ff','#6b41ff','#693fff','#663dff','#643bff','#6138ff','#5f36ff','#5c34ff','#5932ff','#5630ff','#542eff','#502bff','#4d29ff','#4a27ff','#4624ff','#4322ff','#3f1fff','#3a1cff','#3619ff','#3116ff','#2b13ff','#250fff','#1d0aff','#1205ff','#0000ff']


_palette_x = [ImageColor.getrgb(x) for x in _palette_r]
palette = ImagePalette.ImagePalette(palette=[x[0] for x in _palette_x] + [x[1] for x in _palette_x] + [x[2] for x in _palette_x])

def renderPalette(pal):
    """Returns a image rendering of the palette."""
    pal_b = pal.tobytes() # RRR... GGG... BBB...
    R = pal_b[0:256]
    G = pal_b[256:-256]
    B = pal_b[-256:]

    RGB = b''.join(([bytes(c) for c in zip(R,G,B)]))
    im = Image.frombytes(mode='RGB', data=RGB, size=(1,256))

    return im

def filterGridCircle(points, n, radius):
    """Returns points inside circle. Points outside are set to NaN."""
    # Code ported from
    # https://github.com/Smoothieware/Smoothieware/blob/c398f3aa9d2bd6ac2c9328ef0bc08429788d6203/src/modules/tools/zprobe/DeltaGridStrategy.cpp

    res = points.copy()
    d = ((radius * 2) / (n - 1))
    for c in range(n):
        y = -radius + d * c
        for  r in range(n):
            x = -radius + d * r

            distance_from_center = (x * x + y * y)**0.5 # sqrt
            if not distance_from_center <= radius:
                res[c*n+r] = float("NaN")
    
    return res


def render(data, use_palette=True, pixelsize=None, background=(0,0,0,127)):
    grid_size, grid_radius =  struct.unpack("<Bf", data[0:5])

    points = list(struct.unpack("<{}f".format(grid_size**2), data[5:]))
    fpoints = filterGridCircle(points, grid_size, grid_radius)

    # Determine highest and lowest correction point
    cpoints = [p for p in fpoints if not math.isnan(p)]
    lowest = min(cpoints)
    highest = max(cpoints)

    print((lowest, highest))

    offset = 0-lowest
    scale = highest + offset

    scaled = [(x+offset)/scale for x in points]
    clamped = [min(max(0,x),1) for x in scaled]

    # Create image from point data
    greyscale = [x*255 for x in clamped]

    im_b = bytes([round(x) for x in greyscale])

    im = Image.frombytes(mode='P', data=im_b, size=(grid_size,)*2)

    if use_palette:
        im.putpalette(palette)
    
    # Remove points outside the circle
    im = im.convert("RGBA")
    for n, p in enumerate(fpoints):
        xy = divmod(n, grid_size)
        if math.isnan(p):
            im.putpixel(xy, background)

    # Flip X
    im = im.transpose(Image.FLIP_TOP_BOTTOM)

    # Scale grid up
    if not pixelsize:
        pixelsize = 270 // grid_size
    
    rim = im.resize((grid_size * pixelsize,)*2)

    # New image with space for the grid, scale and labels.
    fim = Image.new("RGBA", (340, 286), background)
    fim.paste(rim, (8, (fim.height - rim.height)//2))

    # Add palette scale
    pim = renderPalette(palette).resize((16,256))
    
    pimhpos = (fim.height - pim.height) // 2
    pimwpos = fim.width - pim.width - 8
    fim.paste(pim, (pimwpos, pimhpos))

    # Draw text labels
    fdr = ImageDraw.Draw(fim)
    font = fdr.getfont()

    label = "{:.3f}".format(lowest)
    pos = (pimwpos - 2 - font.getsize(label)[0], pimhpos - (font.getsize(label)[1] // 2))
    fdr.text(pos, label)

    label = "{:.3f}".format(highest)
    pos = (pimwpos - 2 - font.getsize(label)[0], pimhpos + 256 - (font.getsize(label)[1] // 2))
    fdr.text(pos, label)

    return fim
