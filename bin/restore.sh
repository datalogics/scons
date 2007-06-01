#!/usr/bin/env sh
#
# Simple hack script to restore __revision__, __COPYRIGHT_, 0.97
# and other similar variables to what gets checked in to source.  This
# comes in handy when people send in diffs based on the released source.
#

if test "X$*" = "X"; then
    DIRS="src test"
else
    DIRS="$*"
fi

SEPARATOR="================================================================================"

header() {
    arg_space="$1 "
    dots=`echo "$arg_space" | sed 's/./\./g'`
    echo "$SEPARATOR" | sed "s;$dots;$arg_space;"
}

for i in `find $DIRS -name '*.py'`; do
    header $i
    ed $i <<EOF
g/Copyright (c) 2001.*SCons Foundation/s//Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007 The SCons Foundation/p
w
/^__revision__ = /s/= .*/= "/home/scons/scons/branch.0/baseline/bin/restore.sh 0.97.D001 2007/05/17 11:35:19 knight"/p
w
q
EOF
done

for i in `find $DIRS -name 'scons.bat'`; do
    header $i
    ed $i <<EOF
g/Copyright (c) 2001.*SCons Foundation/s//Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007 The SCons Foundation/p
w
/^@REM src\/script\/scons.bat/s/@REM .* knight/@REM /home/scons/scons/branch.0/baseline/bin/restore.sh 0.97.D001 2007/05/17 11:35:19 knight/p
w
q
EOF
done

for i in `find $DIRS -name '__init__.py' -o -name 'scons.py' -o -name 'sconsign.py'`; do
    header $i
    ed $i <<EOF
/^__version__ = /s/= .*/= "0.97"/p
w
/^__build__ = /s/= .*/= "D001"/p
w
/^__buildsys__ = /s/= .*/= "roxbury"/p
w
/^__date__ = /s/= .*/= "2007/05/17 11:35:19"/p
w
/^__developer__ = /s/= .*/= "knight"/p
w
q
EOF
done

for i in `find $DIRS -name 'setup.py'`; do
    header $i
    ed $i <<EOF
/^ *version = /s/= .*/= "0.97",/p
w
q
EOF
done

for i in `find $DIRS -name '*.txt'`; do
    header $i
    ed $i <<EOF
g/Copyright (c) 2001.*SCons Foundation/s//Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007 The SCons Foundation/p
w
/# [^ ]* 0.96.[CD][0-9]* [0-9\/]* [0-9:]* knight$/s/.*/# /home/scons/scons/branch.0/baseline/bin/restore.sh 0.97.D001 2007/05/17 11:35:19 knight/p
w
/Version [0-9][0-9]*\.[0-9][0-9]*/s//Version 0.97/p
w
q
EOF
done

for i in `find $DIRS -name '*.xml'`; do
    header $i
    ed $i <<EOF
g/Copyright (c) 2001.*SCons Foundation/s//Copyright (c) 2001, 2002, 2003, 2004, 2005, 2006, 2007 The SCons Foundation/p
w
q
EOF
done
