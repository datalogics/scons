#!/usr/bin/env python
#
# scons-post-install - SCons post install script for Windows 
#
# A script for configuring "App Paths" registry key so that SCons could
# be run from any directory the same way Python is. 
#

#
# SCons - a Software Constructor
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

__revision__ = "/home/scons/scons/branch.0/baseline/src/script/scons-post-install.py 0.97.D001 2007/05/17 11:35:19 knight"

import os.path
import sys

scons_bat_path = os.path.join(sys.prefix, 'Scripts', 'scons.bat')

app_paths_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\SCons.bat'

def install():
    if sys.platform == 'win32':
        try:
            import _winreg
        except ImportError:
            pass
        else:
            print 'Writing "App Paths" registry entry for %s' % scons_bat_path
            _winreg.SetValue(
                _winreg.HKEY_LOCAL_MACHINE, 
                app_paths_key,
                _winreg.REG_SZ,
                scons_bat_path)
            print 'Done.'


def remove():
    if sys.platform == 'win32':
        try:
            import _winreg
        except ImportError:
            pass
        else:
            # print 'Remove "App Paths" registry entry'
            _winreg.DeleteKey(_winreg.HKEY_LOCAL_MACHINE, app_paths_key)


if len(sys.argv) > 1:
    if sys.argv[1] == '-install':
        install()
    elif sys.argv[1] == '-remove':
        remove()

sys.exit(0)
