#!/usr/bin/env python
#
# __COPYRIGHT__
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

"""
Test the ability to configure the $ASPPCOM construction variable.
"""

import os
import string
import sys
import TestSCons

_python_ = TestSCons._python_

test = TestSCons.TestSCons()



test.write('myas.py', r"""
import sys
infile = open(sys.argv[2], 'rb')
outfile = open(sys.argv[1], 'wb')
for l in filter(lambda l: l != "#as\n", infile.readlines()):
    outfile.write(l)
sys.exit(0)
""")

test.write('SConstruct', """
env = Environment(ASPPCOM = r'%(_python_)s myas.py $TARGET $SOURCE',
                  OBJSUFFIX = '.obj',
                  SHOBJSUFFIX = '.shobj')
env.Object(target = 'test1', source = 'test1.spp')
env.Object(target = 'test2', source = 'test2.SPP')
env.SharedObject(target = 'test3', source = 'test3.spp')
env.SharedObject(target = 'test4', source = 'test4.SPP')
""" % locals())

test.write('test1.spp', "test1.spp\n#as\n")
test.write('test2.SPP', "test2.SPP\n#as\n")
test.write('test3.spp', "test3.spp\n#as\n")
test.write('test4.SPP', "test4.SPP\n#as\n")

test.run(arguments = '.')

test.fail_test(test.read('test1.obj') != "test1.spp\n")
test.fail_test(test.read('test2.obj') != "test2.SPP\n")
test.fail_test(test.read('test3.shobj') != "test3.spp\n")
test.fail_test(test.read('test4.shobj') != "test4.SPP\n")



test.pass_test()
