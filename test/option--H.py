#!/usr/bin/env python
#
# Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007 The SCons Foundation
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

__revision__ = "/home/scons/scons/branch.0/baseline/test/option--H.py 0.97.D001 2007/05/17 11:35:19 knight"

import copy
import string
import sys

import TestSCons

test = TestSCons.TestSCons()

test.write('SConstruct', "")

test.run(arguments = '-H')

test.fail_test(string.find(test.stdout(), '-H, --help-options') == -1)
test.fail_test(string.find(test.stdout(), '--debug=TYPE') == -1)

# Validate that the help output lists the options in case-insensitive
# alphabetical order.
lines = string.split(test.stdout(), '\n')
lines = filter(lambda x: x[:3] == '  -', lines)
lines = map(lambda x: x[3:], lines)
lines = map(lambda x: x[0] == '-' and x[1:] or x, lines)
options = map(lambda x: string.split(x)[0], lines)
options = map(lambda x: x[-1] == ',' and x[:-1] or x, options)
lowered = map(lambda x: string.lower(x), options)
sorted = copy.copy(lowered)
sorted.sort()
test.fail_test(lowered != sorted)

test.pass_test()
 
