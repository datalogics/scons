"""SCons.Environment

XXX

"""

#
# Copyright (c) 2001 Steven Knight
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



import copy
import re
import types
import SCons.Util
import SCons.Builder
from SCons.Errors import UserError

def Command():
    pass	# XXX

def Install():
    pass	# XXX

def InstallAs():
    pass	# XXX



def _deepcopy_atomic(x, memo):
	return x
copy._deepcopy_dispatch[types.ModuleType] = _deepcopy_atomic
copy._deepcopy_dispatch[types.ClassType] = _deepcopy_atomic
copy._deepcopy_dispatch[types.FunctionType] = _deepcopy_atomic
copy._deepcopy_dispatch[types.MethodType] = _deepcopy_atomic
copy._deepcopy_dispatch[types.TracebackType] = _deepcopy_atomic
copy._deepcopy_dispatch[types.FrameType] = _deepcopy_atomic
copy._deepcopy_dispatch[types.FileType] = _deepcopy_atomic



class Environment:
    """Base class for construction Environments.  These are
    the primary objects used to communicate dependency and
    construction information to the build engine.

    Keyword arguments supplied when the construction Environment
    is created are construction variables used to initialize the
    Environment.
    """

    def __init__(self, **kw):
	import SCons.Defaults
	self._dict = copy.deepcopy(SCons.Defaults.ConstructionEnvironment)
	if kw.has_key('BUILDERS') and type(kw['BUILDERS']) != type([]):
	        kw['BUILDERS'] = [kw['BUILDERS']]
        if kw.has_key('SCANNERS') and type(kw['SCANNERS']) != type([]):
                kw['SCANNERS'] = [kw['SCANNERS']]
	self._dict.update(copy.deepcopy(kw))

	class BuilderWrapper:
	    """Wrapper class that allows an environment to
	    be associated with a Builder at instantiation.
	    """
	    def __init__(self, env, builder):
		self.env = env
		self.builder = builder
	
	    def __call__(self, target = None, source = None):
		return self.builder(self.env, target, source)

	    # This allows a Builder to be executed directly
	    # through the Environment to which it's attached.
	    # In practice, we shouldn't need this, because
	    # builders actually get executed through a Node.
	    # But we do have a unit test for this, and can't
	    # yet rule out that it would be useful in the
	    # future, so leave it for now.
	    def execute(self, **kw):
	    	kw['env'] = self
	    	apply(self.builder.execute, (), kw)

	for b in self._dict['BUILDERS']:
	    setattr(self, b.name, BuilderWrapper(self, b))

        for s in self._dict['SCANNERS']:
            setattr(self, s.name, s)

    def __cmp__(self, other):
	return cmp(self._dict, other._dict)

    def Builders(self):
	pass	# XXX

    def Copy(self, **kw):
	"""Return a copy of a construction Environment.  The
	copy is like a Python "deep copy"--that is, independent
	copies are made recursively of each objects--except that
	a reference is copied when an object is not deep-copyable
	(like a function).  There are no references to any mutable
	objects in the original Environment.
	"""
	clone = copy.deepcopy(self)
	apply(clone.Update, (), kw)
	return clone

    def Scanners(self):
	pass	# XXX

    def	Update(self, **kw):
	"""Update an existing construction Environment with new
	construction variables and/or values.
	"""
	self._dict.update(copy.deepcopy(kw))

    def	Depends(self, target, dependency):
	"""Explicity specify that 'target's depend on 'dependency'."""
	tlist = SCons.Util.scons_str2nodes(target)
	dlist = SCons.Util.scons_str2nodes(dependency)
	for t in tlist:
	    t.add_dependency(dlist)

	if len(tlist) == 1:
	    tlist = tlist[0]
	return tlist

    def Dictionary(self, *args):
	if not args:
	    return self._dict
	dlist = map(lambda x, s=self: s._dict[x], args)
	if len(dlist) == 1:
	    dlist = dlist[0]
	return dlist

    def Command(self, target, source, action):
        """Builds the supplied target files from the supplied
        source files using the supplied action.  Action may
        be any type that the Builder constructor will accept
        for an action."""
        bld = SCons.Builder.Builder(name="Command", action=action)
        return bld(self, target, source)

    def subst(self, string):
	"""Recursively interpolates construction variables from the
	Environment into the specified string, returning the expanded
	result.  Construction variables are specified by a $ prefix
	in the string and begin with an initial underscore or
	alphabetic character followed by any number of underscores
	or alphanumeric characters.  The construction variable names
	may be surrounded by curly braces to separate the name from
	trailing characters.
	"""
	return SCons.Util.scons_subst(string, self._dict, {})

    def get_scanner(self, skey):
        """Find the appropriate scanner given a key (usually a file suffix).
        Does a linear search. Could be sped up by creating a dictionary if
        this proves too slow.
        """
        if self._dict['SCANNERS']:
            for scanner in self._dict['SCANNERS']:
                if skey in scanner.skeys:
                    return scanner
        return None
