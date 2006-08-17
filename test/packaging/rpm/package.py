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
Test the ability to create a really simple rpm package.
"""

import os
import TestSCons

python = TestSCons.python

test = TestSCons.TestSCons()

rpm = test.Environment().WhereIs('rpm')

if rpm:
  test.subdir('src')

  test.write( [ 'src', 'main.c' ], r"""
int main( int argc, char* argv[] )
{
  return 0;
}
  """)

  test.write('SConstruct', """
import os

prog = Install( '/bin/' , Program( 'src/main.c')  )

Package( projectname    = 'foo',
         version        = '1.2.3',
         packageversion = 0,
         type           = 'rpm',
         license        = 'gpl',
         summary        = 'balalalalal',
         x_rpm_Group    = 'Application/fu',
         description    = 'this should be reallly really long',
         source         = [ prog ],
         source_url     = 'http://foo.org/foo-1.2.3.tar.gz'
        )

Alias( 'install', prog )
""")

  test.run(arguments='', stderr = None)

  test.fail_test( not os.path.exists( 'foo-1.2.3-0.i386.rpm' ) )
  test.fail_test( not os.path.exists( 'foo-1.2.3-0.src.rpm' ) )
  test.fail_test( not os.popen('rpm -qpl foo-1.2.3-0.i386.rpm').read()=='/bin/main\n')
  test.fail_test( not os.popen('rpm -qpl foo-1.2.3-0.src.rpm').read()=='foo-1.2.3.spec\nfoo-1.2.3.tar.gz\n')
  test.fail_test( os.path.exists( 'bin/main' ) )

test.pass_test()
