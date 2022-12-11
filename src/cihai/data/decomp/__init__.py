#!/usr/bin/env python
"""Chinese character decomposition.

cihai.datasets.decomp
~~~~~~~~~~~~~~~~~~~~~

See http://cjkdecomp.codeplex.com/wikipage?title=cjk-decomp&referringTitle=Home

The CJK Decomposition Data File is a graphical analysis of the approx 75,000
Chinese/Japanese characters in Unicode. The latest version is 0.4.0, updated on
15 August 2012.

The data comprises the 36 strokes (0x31c0..0x31e3), the 115 radicals
(0x2e80..0x2ef3, except 0x2e9a), the 20924 unified characters (0x4e00..0x9fbb),
the 12 unique characters from the compatibility range (0xf900..0xfad9), the
6582 extension A characters (0x3400..0x4db5), the 42711 extension B characters
(0x20000..0x2a6d6), the 4149 extension C characters (0x2a700..0x2b734), and the
222 extension D characters (0x2b740..0x2b81d).

Each record has 3 fields, viz, the character being defined, the type of
decomposition, and a list of zero or more constituent components, like so:

的:a(白,勺)

The character being defined and the constituent components are either a Unihan
token, in the basic or a supplemental plane, or a 5-digit number representing
an intermediate decomposition not in Unicode. There are approx 10,000 such
intermediate decompositions.

If you need a font, you can use the Hanazono font.

Only pictorial configurations are used, not semantic ones. Where characters
have typeface differences I've used the one provided by the Mainland Chinese
contribution to Unicode. When there's more than one possible configuration,
I've selected one only.

The possible configurations and their meanings are:
Code regex       Meaning         Number of possible constituents
c        component       0
m.*      modified in some way, e.g. me=equivalent, msp=special, mo=outline, \
         ml=left radical version      1
w.*      second constituent contained within first in some way, e.g. w=within \
         at the center, wbl=within at bottom left   2
ba|d     second between first moving across or downwards         2
lock     components locked together      2
s.*      first component surrounds second, e.g. s=surrounds fully, \
         str=surrounds around the top-right    2
a        flows across    >= 2
d        flows downwards         >= 2
r.*      repeats and/or reflects in some way, e.g. refh=reflect horizontally, \
         rot=rotate 180 degrees, rrefr= repeat with a reflection rightwards, \
         ra=repeat across, r3d=repeat 3 times downwards, r3tr=repeat in a \
         triangle, rst=repeat surrounding around the top       1


The s, a, d, and r codes may be followed by /t, /m, /s, or /o, to show whether
the join touches, molds, snaps together, or overlaps, respectively.

Some more work needs to be done, including reducing the quantity of
intermediate components by removing duplicates, lowering the number of
components in many sequences, reanalysis of decomposition configurations, and
of course quality checking and corrections.

Last edited Dec 6, 2013 at 8:09 PM by gavingrover, version 3

"""
import logging

__copyright__ = "Copyright 2013-2018 Tony Narlock."
__license__ = "MIT, see LICENSE for details."

log = logging.getLogger(__name__)
