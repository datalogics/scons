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
Test the --package-type option.
"""

import TestSCons

machine = TestSCons.machine
_python_ = TestSCons._python_

test = TestSCons.TestSCons()

scons = test.program

rpm = test.Environment().WhereIs('rpm')

if not rpm:
    test.skip_test('rpm not found, skipping test\n')

test.subdir('src')

test.write( 'main', '' )

test.write('SConstruct', """
# -*- coding: iso-8859-15 -*-
env=Environment(tools=['default', 'packaging'])
env.Prepend(RPM = 'TAR_OPTIONS=--wildcards ')
prog=env.Install( '/bin', 'main' )
env.Package( NAME           = 'foo',
             VERSION        = '1.2.3',
             LICENSE        = 'gpl',
             SUMMARY        = 'hello',
             PACKAGEVERSION = 0,
             X_RPM_GROUP    = 'Application/office',
             X_RPM_INSTALL  = r'%(_python_)s %(scons)s --install-sandbox="$RPM_BUILD_ROOT" "$RPM_BUILD_ROOT"',
             DESCRIPTION    = 'this should be really long',
             source         = [ prog ],
             SOURCE_URL     = 'http://foo.org/foo-1.2.3.tar.gz'
            )
""" % locals())

test.run(arguments='package PACKAGETYPE=rpm', stderr = None)

src_rpm = 'foo-1.2.3-0.src.rpm'
machine_rpm = 'foo-1.2.3-0.%s.rpm' % machine

test.must_exist( src_rpm )
test.must_exist( machine_rpm )

test.must_not_exist( 'bin/main.c' )
test.must_not_exist( '/bin/main.c' )

test.pass_test()
