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

import os
import sys

import TestCmd
import TestSCons

python = TestSCons.python

test = TestSCons.TestSCons()

test_config1 = test.workpath('test-config1')
test_config2 = test.workpath('test-config2')

# 'abc' is supposed to be a static lib; it is included in LIBS as a
# File node.
# It used to be returned as the 'static_libs' output of ParseConfig.
test.write(test_config1, """\
print "-I/usr/include/fum -Ibar -X"
print "-L/usr/fax -Lfoo -lxxx abc"
""")

test.write(test_config2, """\
print "-L foo -L lib_dir"
""")

test.write('SConstruct', """
env = Environment(CPPPATH = [], LIBPATH = [], LIBS = [], CCFLAGS = '')
env.ParseConfig([r"%(python)s", r"%(test_config1)s", "--libs --cflags"])
env.ParseConfig([r"%(python)s", r"%(test_config2)s", "--libs --cflags"])
print env['CPPPATH']
print env['LIBPATH']
print map(lambda x: str(x), env['LIBS'])
print env['CCFLAGS']
""" % locals())

test.write('SConstruct2', """
env = Environment(CPPPATH = [], LIBPATH = [], LIBS = [], CCFLAGS = '',
                  PYTHON = '%(python)s')
env.ParseConfig(r"$PYTHON %(test_config1)s --libs --cflags")
env.ParseConfig(r"$PYTHON %(test_config2)s --libs --cflags")
print env['CPPPATH']
print env['LIBPATH']
print map(lambda x: str(x), env['LIBS'])
print env['CCFLAGS']
""" % locals())

good_stdout = test.wrap_stdout(read_str = """\
['/usr/include/fum', 'bar']
['/usr/fax', 'foo', 'lib_dir']
['xxx', 'abc']
['-X']
""", build_str = "scons: `.' is up to date.\n")

test.run(arguments = ".", stdout = good_stdout)

test.run(arguments = "-f SConstruct2 .", stdout = good_stdout)

test.pass_test()
