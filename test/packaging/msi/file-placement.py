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
Test the msi packagers ability to put files into distinct directories.
"""

import os
import TestSCons
from xml.dom.minidom import *

python = TestSCons.python

test = TestSCons.TestSCons()

wix = test.Environment().WhereIs('candle')

if wix:
  #
  # Test the default directory layout
  #
  test.write( 'file1.exe', "file1" )

  test.write('SConstruct', """
import os

f1 = Install( '/bin/' , 'file1.exe'  )

Package( projectname    = 'foo',
         version        = '1.2',
         type           = 'msi',
         summary        = 'balalalalal',
         description    = 'this should be reallly really long',
         vendor         = 'Nanosoft_2000',
         source         = [ f1 ],
        )
""")

  test.run(arguments='', stderr = None)

  dom  = parse( test.workpath( 'foo-1.2.wxs' ) )
  dirs = dom.getElementsByTagName( 'Directory' )

  test.fail_test( not dirs[0].attributes['Name'].value == 'SourceDir' )
  test.fail_test( not dirs[1].attributes['Name'].value == 'PFiles' )
  test.fail_test( not dirs[2].attributes['Name'].value == 'NANOSO~1' )
  test.fail_test( not dirs[3].attributes['Name'].value == 'FOO-1.2' )

  #
  # Try to put 7 files into 5 distinct directories of varying depth and overlapping count
  #
  test.write( 'file1.exe', "file1" )
  test.write( 'file2.exe', "file2" )
  test.write( 'file3.dll', "file3" )
  test.write( 'file4.dll', "file4" )
  test.write( 'file5.class', "file5" )
  test.write( 'file6.class', "file6" )
  test.write( 'file7.class', "file7" )

  test.write('SConstruct', """
import os

f1 = Install( '/bin/' , 'file1.exe'  )
f2 = Install( '/bin/' , 'file2.exe'  )
f3 = Install( '/lib/' , 'file3.dll'  )
f4 = Install( '/lib/' , 'file4.dll'  )
f5 = Install( '/java/edu/teco/' , 'file5.class'  )
f6 = Install( '/java/teco/' , 'file6.class'  )
f7 = Install( '/java/tec/' , 'file7.class'  )

Package( projectname    = 'foo',
         version        = '1.2',
         type           = 'msi',
         summary        = 'balalalalal',
         description    = 'this should be reallly really long',
         vendor         = 'Nanosoft_2000',
         license        = 'afl',
         source         = [ f1, f2, f3, f4, f5, f6, f7 ],
        )
""")

  test.run(arguments='', stderr = None)

  dom   = parse( test.workpath( 'foo-1.2.wxs' ) )
  files = dom.getElementsByTagName( 'File' )

  test.fail_test( not files[0].parentNode.parentNode.attributes['LongName'].value == 'bin' )
  test.fail_test( not files[1].parentNode.parentNode.attributes['LongName'].value == 'bin' )
  test.fail_test( not files[2].parentNode.parentNode.attributes['LongName'].value == 'lib' )
  test.fail_test( not files[3].parentNode.parentNode.attributes['LongName'].value == 'lib' )
    
  test.fail_test( not files[4].parentNode.parentNode.attributes['LongName'].value == 'teco' )
  test.fail_test( not files[4].parentNode.parentNode.parentNode.attributes['LongName'].value == 'edu' )
  test.fail_test( not files[4].parentNode.parentNode.parentNode.parentNode.attributes['LongName'].value == 'java' )

  test.fail_test( not files[5].parentNode.parentNode.attributes['LongName'].value == 'teco' )
  test.fail_test( not files[5].parentNode.parentNode.parentNode.attributes['LongName'].value == 'java' )

  test.fail_test( not files[6].parentNode.parentNode.attributes['LongName'].value == 'tec' )
  test.fail_test( not files[6].parentNode.parentNode.parentNode.attributes['LongName'].value == 'java' )

  #
  # Test distinct directories put into distinct features
  #
  test.write( 'file1.exe', "file1" )
  test.write( 'file2.exe', "file2" )
  test.write( 'file3.dll', "file3" )

  test.write('SConstruct', """
import os

f1 = Install( '/bin/' , 'file1.exe'  )
f2 = Install( '/bin/' , 'file2.exe'  )
f3 = Install( '/lib/' , 'file3.dll'  )

Tag( [f1, f2], x_msi_feature = 'Core Part' )
Tag( f3, x_msi_feature = 'Java Part' )

Package( projectname    = 'foo',
         version        = '1.2',
         type           = 'msi',
         summary        = 'balalalalal',
         description    = 'this should be reallly really long',
         vendor         = 'Nanosoft_2000',
         license        = 'afl',
         source         = [ f1, f2, f3 ],
        )
""")

  test.run(arguments='', stderr = None)

  dom      = parse( test.workpath( 'foo-1.2.wxs' ) )
  features = dom.getElementsByTagName( 'Feature' )

  test.fail_test( not features[1].attributes['Title'].value == 'Core Part' )
  componentrefs = features[1].getElementsByTagName( 'ComponentRef' ) 
  test.fail_test( not componentrefs[0].attributes['Id'].value == 'fileexe_a' )
  test.fail_test( not componentrefs[1].attributes['Id'].value == 'fileexe_b' )

  test.fail_test( not features[2].attributes['Title'].value == 'Java Part' )
  componentrefs = features[2].getElementsByTagName( 'ComponentRef' ) 
  test.fail_test( not componentrefs[0].attributes['Id'].value == 'filedll_a' )

test.pass_test()
