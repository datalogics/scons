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
import sys
import TestCmd
import unittest

import SCons.dblite

import SCons.SConsign

class BuildInfo:
    def __init__(self, name):
        self.name = name
    def convert_to_sconsign(self):
        self.c_to_s = 1
    def convert_from_sconsign(self, dir, name):
        self.c_from_s = 1

class DummyModule:
    def to_string(self, sig):
        return str(sig)

    def from_string(self, sig):
        return int(sig)

class FS:
    def __init__(self, top):
        self.Top = top
        self.Top.repositories = []

class DummyNode:
    def __init__(self, path='not_a_valid_path'):
        self.path = path
        self.tpath = path
        self.fs = FS(self)

class SConsignTestCase(unittest.TestCase):
    def setUp(self):
        self.save_cwd = os.getcwd()
        self.test = TestCmd.TestCmd(workdir = '')
        os.chdir(self.test.workpath(''))
    def tearDown(self):
        self.test.cleanup()
        SCons.SConsign.Reset()
        os.chdir(self.save_cwd)

class BaseTestCase(SConsignTestCase):

    def runTest(self):
        aaa = BuildInfo('aaa')
        bbb = BuildInfo('bbb')
        bbb.arg1 = 'bbb arg1'
        ccc = BuildInfo('ccc')
        ccc.arg2 = 'ccc arg2'

        f = SCons.SConsign.Base()
        f.set_entry('aaa', aaa)
        f.set_entry('bbb', bbb)

        e = f.get_entry('aaa')
        assert e == aaa, e
        assert e.name == 'aaa', e.name

        e = f.get_entry('bbb')
        assert e == bbb, e
        assert e.name == 'bbb', e.name
        assert e.arg1 == 'bbb arg1', e.arg1
        assert not hasattr(e, 'arg2'), e

        f.set_entry('bbb', ccc)
        e = f.get_entry('bbb')
        assert e.name == 'ccc', e.name
        assert not hasattr(e, 'arg1'), e
        assert e.arg2 == 'ccc arg2', e.arg1

        ddd = BuildInfo('ddd')
        eee = BuildInfo('eee')
        fff = BuildInfo('fff')
        fff.arg = 'fff arg'

        f = SCons.SConsign.Base(DummyModule())
        f.set_entry('ddd', ddd)
        f.set_entry('eee', eee)

        e = f.get_entry('ddd')
        assert e == ddd, e
        assert e.name == 'ddd', e.name

        e = f.get_entry('eee')
        assert e == eee, e
        assert e.name == 'eee', e.name
        assert not hasattr(e, 'arg'), e

        f.set_entry('eee', fff)
        e = f.get_entry('eee')
        assert e.name == 'fff', e.name
        assert e.arg == 'fff arg', e.arg

class SConsignDBTestCase(SConsignTestCase):

    def runTest(self):
        save_DataBase = SCons.SConsign.DataBase
        SCons.SConsign.DataBase = {}
        try:
            d1 = SCons.SConsign.DB(DummyNode('dir1'))
            d1.set_entry('aaa', BuildInfo('aaa name'))
            d1.set_entry('bbb', BuildInfo('bbb name'))
            aaa = d1.get_entry('aaa')
            assert aaa.name == 'aaa name'
            bbb = d1.get_entry('bbb')
            assert bbb.name == 'bbb name'

            d2 = SCons.SConsign.DB(DummyNode('dir2'))
            d2.set_entry('ccc', BuildInfo('ccc name'))
            d2.set_entry('ddd', BuildInfo('ddd name'))
            ccc = d2.get_entry('ccc')
            assert ccc.name == 'ccc name'
            ddd = d2.get_entry('ddd')
            assert ddd.name == 'ddd name'

            d31 = SCons.SConsign.DB(DummyNode('dir3/sub1'))
            d31.set_entry('eee', BuildInfo('eee name'))
            d31.set_entry('fff', BuildInfo('fff name'))
            eee = d31.get_entry('eee')
            assert eee.name == 'eee name'
            fff = d31.get_entry('fff')
            assert fff.name == 'fff name'

            d32 = SCons.SConsign.DB(DummyNode('dir3%ssub2' % os.sep))
            d32.set_entry('ggg', BuildInfo('ggg name'))
            d32.set_entry('hhh', BuildInfo('hhh name'))
            ggg = d32.get_entry('ggg')
            assert ggg.name == 'ggg name'
            hhh = d32.get_entry('hhh')
            assert hhh.name == 'hhh name'
        finally:
            SCons.SConsign.DataBase = save_DataBase

class SConsignDirFileTestCase(SConsignTestCase):

    def runTest(self):
        bi_foo = BuildInfo('foo')
        bi_bar = BuildInfo('bar')

        f = SCons.SConsign.DirFile(DummyNode(), DummyModule())
        f.set_entry('foo', bi_foo)
        f.set_entry('bar', bi_bar)

        e = f.get_entry('foo')
        assert e == bi_foo, e
        assert e.name == 'foo', e.name

        assert bi_foo.c_from_s, bi_foo.c_from_s

        e = f.get_entry('bar')
        assert e == bi_bar, e
        assert e.name == 'bar', e.name
        assert not hasattr(e, 'arg'), e

        assert bi_bar.c_from_s, bi_bar.c_from_s

        bbb = BuildInfo('bbb')
        bbb.arg = 'bbb arg'
        f.set_entry('bar', bbb)
        e = f.get_entry('bar')
        assert e.name == 'bbb', e.name
        assert e.arg == 'bbb arg', e.arg


class SConsignFileTestCase(SConsignTestCase):

    def runTest(self):
        test = self.test
        file = test.workpath('sconsign_file')

        assert SCons.SConsign.DataBase == {}, SCons.SConsign.DataBase
        assert SCons.SConsign.DB_Name == ".sconsign", SCons.SConsign.DB_Name
        assert SCons.SConsign.DB_Module is SCons.dblite, SCons.SConsign.DB_Module

        SCons.SConsign.File(file)

        assert SCons.SConsign.DataBase == {}, SCons.SConsign.DataBase
        assert SCons.SConsign.DB_Name is file, SCons.SConsign.DB_Name
        assert SCons.SConsign.DB_Module is SCons.dblite, SCons.SConsign.DB_Module

        SCons.SConsign.File(None)

        assert SCons.SConsign.DataBase == {}, SCons.SConsign.DataBase
        assert SCons.SConsign.DB_Name is file, SCons.SConsign.DB_Name
        assert SCons.SConsign.DB_Module is None, SCons.SConsign.DB_Module

        class Fake_DBM:
            def open(self, name, mode):
                self.name = name
                self.mode = mode
                return self
            def __getitem__(self, key):
                pass
            def __setitem__(self, key, value):
                pass

        fake_dbm = Fake_DBM()

        SCons.SConsign.File(file, fake_dbm)

        assert SCons.SConsign.DataBase == {}, SCons.SConsign.DataBase
        assert SCons.SConsign.DB_Name is file, SCons.SConsign.DB_Name
        assert SCons.SConsign.DB_Module is fake_dbm, SCons.SConsign.DB_Module
        assert not hasattr(fake_dbm, 'name'), fake_dbm
        assert not hasattr(fake_dbm, 'mode'), fake_dbm

        SCons.SConsign.ForDirectory(DummyNode(test.workpath('dir')))

        assert not SCons.SConsign.DataBase is None, SCons.SConsign.DataBase
        assert fake_dbm.name == file, fake_dbm.name
        assert fake_dbm.mode == "c", fake_dbm.mode


class writeTestCase(SConsignTestCase):

    def runTest(self):

        test = self.test
        file = test.workpath('sconsign_file')

        class Fake_DBM:
            def __getitem__(self, key):
                return None
            def __setitem__(self, key, value):
                pass
            def open(self, name, mode):
                self.sync_count = 0
                return self
            def sync(self):
                self.sync_count = self.sync_count + 1

        fake_dbm = Fake_DBM()

        SCons.SConsign.DataBase = {}
        SCons.SConsign.File(file, fake_dbm)

        f = SCons.SConsign.DB(DummyNode(), DummyModule())

        bi_foo = BuildInfo('foo')
        bi_bar = BuildInfo('bar')
        f.set_entry('foo', bi_foo)
        f.set_entry('bar', bi_bar)

        SCons.SConsign.write()

        assert bi_foo.c_to_s, bi_foo.c_to_s
        assert bi_bar.c_to_s, bi_bar.c_to_s

        assert fake_dbm.sync_count == 1, fake_dbm.sync_count


def suite():
    suite = unittest.TestSuite()
    suite.addTest(BaseTestCase())
    suite.addTest(SConsignDBTestCase())
    suite.addTest(SConsignDirFileTestCase())
    suite.addTest(SConsignFileTestCase())
    suite.addTest(writeTestCase())
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    result = runner.run(suite())
    if not result.wasSuccessful():
        sys.exit(1)

