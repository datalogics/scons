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

"""SCons.Warnings

This file implements the warnings framework for SCons.

"""

__revision__ = "__FILE__ __REVISION__ __DATE__ __DEVELOPER__"

import string
import sys

import SCons.Errors

from SCons.i18n import _


class Warning(SCons.Errors.UserError):
    pass

class MandatoryWarning(Warning):
    pass



class FutureDeprecatedWarning(Warning):
    pass

class DeprecatedWarning(Warning):
    pass

class MandatoryDeprecatedWarning(MandatoryWarning):
    pass



# NOTE:  If you add a new warning class, add it to the man page, too!

class CacheWriteErrorWarning(Warning):
    pass

class CorruptSConsignWarning(Warning):
    pass

class DependencyWarning(Warning):
    pass

class DeprecatedCopyWarning(DeprecatedWarning):
    pass

class DeprecatedOptionsWarning(DeprecatedWarning):
    pass

class DeprecatedSourceSignaturesWarning(DeprecatedWarning):
    pass

class DeprecatedTargetSignaturesWarning(DeprecatedWarning):
    pass

class DuplicateEnvironmentWarning(Warning):
    pass

class FutureReservedVariableWarning(Warning):
    pass

class LinkWarning(Warning):
    pass

class MisleadingKeywordsWarning(Warning):
    pass

class MissingSConscriptWarning(Warning):
    pass

class NoMD5ModuleWarning(Warning):
    pass

class NoMetaclassSupportWarning(Warning):
    pass

class NoObjectCountWarning(Warning):
    pass

class NoParallelSupportWarning(Warning):
    pass

class PythonVersionWarning(DeprecatedWarning):
    pass

class ReservedVariableWarning(Warning):
    pass

class StackSizeWarning(Warning):
    pass

class TaskmasterNeedsExecuteWarning(FutureDeprecatedWarning):
    pass

class FortranCxxMixWarning(LinkWarning):
    pass

_warningAsException = 0

# The below is a list of 2-tuples.  The first element is a class object.
# The second element is true if that class is enabled, false if it is disabled.
_enabled = []

_warningOut = None

def suppressWarningClass(clazz):
    """Suppresses all warnings that are of type clazz or
    derived from clazz."""
    _enabled.insert(0, (clazz, 0))

def enableWarningClass(clazz):
    """Suppresses all warnings that are of type clazz or
    derived from clazz."""
    _enabled.insert(0, (clazz, 1))

def warningAsException(flag=1):
    """Turn warnings into exceptions.  Returns the old value of the flag."""
    global _warningAsException
    old = _warningAsException
    _warningAsException = flag
    return old

def warn(clazz, *args):
    global _enabled, _warningAsException, _warningOut

    warning = clazz(args)
    for clazz, flag in _enabled:
        if isinstance(warning, clazz):
            if flag:
                if _warningAsException:
                    raise warning

                if _warningOut:
                    _warningOut(warning)
            break

def process_warn_strings(arguments):
    """Process string specifications of enabling/disabling warnings,
    as passed to the --warn option or the SetOption('warn') function.


    An argument to this option should be of the form <warning-class>
    or no-<warning-class>.  The warning class is munged in order
    to get an actual class name from the classes above, which we
    need to pass to the {enable,disable}WarningClass() functions.
    The supplied <warning-class> is split on hyphens, each element
    is capitalized, then smushed back together.  Then the string
    "Warning" is appended to get the class name.

    For example, 'deprecated' will enable the DeprecatedWarning
    class.  'no-dependency' will disable the .DependencyWarning
    class.

    As a special case, --warn=all and --warn=no-all will enable or
    disable (respectively) the base Warning class of all warnings.

    """

    def _capitalize(s):
        if s[:5] == "scons":
            return "SCons" + s[5:]
        else:
            return string.capitalize(s)

    for arg in arguments:

        elems = string.split(string.lower(arg), '-')
        enable = 1
        if elems[0] == 'no':
            enable = 0
            del elems[0]

        if len(elems) == 1 and elems[0] == 'all':
            class_name = "Warning"
        else:
            class_name = string.join(map(_capitalize, elems), '') + "Warning"
        try:
            clazz = globals()[class_name]
        except KeyError:
            sys.stderr.write(_("No warning type: '%s'\n") % arg)
        else:
            if enable:
                enableWarningClass(clazz)
            elif issubclass(clazz, MandatoryDeprecatedWarning):
                fmt = _("Can not disable mandataory warning: '%s'\n")
                sys.stderr.write(fmt % arg)
            else:
                suppressWarningClass(clazz)

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
