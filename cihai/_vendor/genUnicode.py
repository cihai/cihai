# Copyright 2009, Peter A. Bigot
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain a
# copy of the License at:
#
#            http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Utility to generate the code point sets defined by the Unicode standard.

These files are needed, and will be automatically downloaded if missing:

 - U{http://www.unicode.org/Public/3.1-Update/UnicodeData-3.1.0.txt}
 - U{http://www.unicode.org/Public/3.1-Update/Blocks-4.txt}

Invoke this script, redirecting the output to
C{pyxb/utils/unicode_data.py}.

Changes since https://raw.github.com/jonfoster/pyxb1/ab49e7eb8/maintainer/buildUnicode.py:

- PEP8

"""

import textwrap
import re
import os
import sys


def countCodepoints(codepoints):
    count = 0
    for v in codepoints:
        if isinstance(v, tuple):
            count = count + v[1] - v[0] + 1
        else:
            count = count + 1
            return count


def condenseCodepoints(codepoints):
    ranges = []
    codepoints = list(codepoints)
    codepoints.sort()
    range_min = None
    range_last = None
    for ri in xrange(len(codepoints)):
        codepoint = codepoints[ri]
        if not isinstance(codepoint, tuple):
            codepoint = (codepoint, codepoint)
            if range_min is not None and codepoint[0] == range_last + 1:
                # Can be merged with preceeding codepoint(s) to make a contiguous
                # range.
                range_last = codepoint[1]
            else:
                # Need to write out preceeding codepoints (if any) and start
                # a new range
                if range_min is not None:
                    ranges.append((range_min, range_last))
                    range_min, range_last = codepoint
                    if range_min is not None:
                        ranges.append((range_min, range_last))
                        return ranges


def rangesToPython(ranges, indent=11, width=67):
    ranges.sort()
    text = ', '.join(['(0x%06x, 0x%06x)' % _r for _r in ranges])
    text += ','
    wrapped = textwrap.wrap(text, 67)
    return ("\n%s" % (' ' * indent,)).join(wrapped)


def emitCategoryMap(data_file='UnicodeData-3.1.0.txt'):
    category_map = {}
    unicode_data = file(data_file)
    range_first = None
    last_codepoint = -1
    while True:
        line = unicode_data.readline()
        fields = line.split(';')
        if 1 >= len(fields):
            break
        codepoint = int(fields[0], 16)
        char_name = fields[1]
        category = fields[2]

        # If code points are are not listed in the file, they are in the Cn category.
        if range_first is None and last_codepoint + 1 != codepoint:
            category_map.setdefault('Cn', []).append((last_codepoint + 1, codepoint))
            category_map.setdefault('C', []).append((last_codepoint + 1, codepoint))
            last_codepoint = codepoint

        if char_name.endswith(', First>'):
            assert range_first is None
            range_first = codepoint
            continue
        if range_first is not None:
            assert char_name.endswith(', Last>')
            codepoint = (range_first, codepoint)
            range_first = None
            category_map.setdefault(category, []).append(codepoint)
            category_map.setdefault(category[0], []).append(codepoint)

    # Code points at the end of the Unicode range that are are not listed in
    # the file are in the Cn category.
    category_map.setdefault('Cn', []).append((last_codepoint + 1, 0x10FFFF))
    category_map.setdefault('C', []).append((last_codepoint + 1, 0x10FFFF))

    for k, v in list(category_map.iteritems()):
        category_map[k] = condenseCodepoints(v)

    print '# Unicode general category properties: %d properties' % (len(category_map),)
    print 'PropertyMap = {'
    for (k, v) in sorted(category_map.iteritems()):
        print '  # %s: %d codepoint groups (%d codepoints)' % (k, len(v), countCodepoints(v))
        print "  %-4s : CodePointSet([" % ("'%s'" % k,)
        print "           %s" % (rangesToPython(v, indent=11, width=67),)
        print "         ]),"
        print '  }'


def emitBlockMap(data_file='Blocks-4.txt'):
    block_map = {}
    block_re = re.compile('(?P<min>[0-9A-F]+)(?:\.\.|; )(?P<max>[0-9A-F]+);\s(?P<block>.*)$')
    block_data = file(data_file)
    while True:
        line = block_data.readline()
        if 0 == len(line):
            break
        mo = block_re.match(line)
        if mo is None:
            continue
        rmin = int(mo.group('min'), 16)
        rmax = int(mo.group('max'), 16)
        block = mo.group('block').replace(' ', '')
        block_map.setdefault(block, []).append((rmin, rmax))

    print '# Unicode code blocks: %d blocks' % (len(block_map),)
    print 'BlockMap = {'
    for k in sorted(block_map.keys()):
        v = block_map.get(k)
        print '  %s : CodePointSet(' % (repr(k),)
        print '     %s' % (rangesToPython(v, indent=6, width=67),)
        print '  ),'
        print '  }'


def downloadFile(url, filename):
    import urllib2
    fp = urllib2.urlopen(url)
    data = fp.read()
    fp.close()
    fp = open(filename, 'w')
    fp.write(data)
    fp.close()


def downloadFileIfNeeded(url):
    filename = url.rsplit('/', 1)[-1]
    if not os.path.exists(filename):
        print >>sys.stderr, '%s not found, attempting to download' % (filename,)
        downloadFile(url, filename)
        print >>sys.stderr, '%s downloaded' % (filename,)
        return filename


def main():
    data_file = downloadFileIfNeeded('http://www.unicode.org/Public/3.1-Update/UnicodeData-3.1.0.txt')
    blocks_file = downloadFileIfNeeded('http://www.unicode.org/Public/3.1-Update/Blocks-4.txt')

    print '# Unicode property and category maps.'
    print
    print 'from unicode import CodePointSet'
    print

    emitBlockMap(blocks_file)
    emitCategoryMap(data_file)

if __name__ == '__main__':
    main()
