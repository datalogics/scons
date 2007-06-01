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

__revision__ = "/home/scons/scons/branch.0/baseline/test/Help.py 0.97.D001 2007/05/17 11:35:19 knight"

import TestSCons

test = TestSCons.TestSCons()

wpath = test.workpath()

test.write('SConstruct', r"""
Help("Help text\ngoes here.\n")
""")

expect = """scons: Reading SConscript files ...
scons: done reading SConscript files.
Help text
goes here.

Use scons -H for help about command-line options.
"""

test.run(arguments = '-h', stdout = expect)

test.write('SConstruct', r"""
env = Environment(MORE='more', HELP='help')
env.Help("\nEven $MORE\n$HELP text!\n")
""")

expect = """scons: Reading SConscript files ...
scons: done reading SConscript files.

Even more
help text!

Use scons -H for help about command-line options.
"""

test.run(arguments = '-h', stdout = expect)

test.write('SConstruct', r"""
Help('\nMulti')
Help('line\n')
Help('''\
help
text!
''')
""")

expect = """\
scons: Reading SConscript files ...
scons: done reading SConscript files.

Multiline
help
text!

Use scons -H for help about command-line options.
"""

test.run(arguments = '-h', stdout = expect)

test.pass_test()
