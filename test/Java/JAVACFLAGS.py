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
import string

import TestSCons

test = TestSCons.TestSCons()

ENV = test.java_ENV()

if test.detect_tool('javac', ENV=ENV):
    where_javac = test.detect('JAVAC', 'javac', ENV=ENV)
else:
    where_javac = test.where_is('javac')
if not where_javac:
    test.skip_test("Could not find Java javac, skipping test(s).\n")

test.subdir('src')

test.write('SConstruct', """
env = Environment(tools = ['javac'],
                  JAVAC = r'%(where_javac)s',
                  JAVACFLAGS = '-O')
env.Java(target = 'classes', source = 'src')
""" % locals())

test.write(['src', 'Example1.java'], """\
package src;

public class Example1
{

     public static void main(String[] args)
     {

     }

}
""")

expected_wrapper_out = "%(where_javac)s -O -d classes -sourcepath src src/Example1.java\n"
expected_wrapper_out = string.replace(expected_wrapper_out, '/', os.sep)
test.run(arguments = '.',
         stdout = test.wrap_stdout(expected_wrapper_out % locals()))

test.must_exist(['classes', 'src', 'Example1.class'])

test.pass_test()
