'''
Created on Sep 11, 2013

@author: yali
'''
import unittest
import minify


class MinifyTest(unittest.TestCase):

    def testShellExec(self):
        pass

    def testIsMinified(self):
        minifiedFiles = [
                         'a.min.ext', 'a-min.ext', # extension doesn't matter
                         '.min.ext', '-min.ext', # only sub-ext and ext in the file name
                         'abc.min.js', 'abc.min.css', # normal
                         'abc-min.js', 'abc-min.css', # normal
                         r'c:\a\bc.min.ext', '/a/b/c/d-min.ext' # full path
                         ]
        unminifiedFiles = [
                         'a.ext', 'a-.ext', # extension doesn't matter
                         '..ext', '-.ext', # only sub-ext and ext in the file name
                         'abc..js', 'abc..css', # normal
                         'abc-.js', 'abc-.css', # normal
                         r'c:\a\bc..ext', '/a/b/c/d-.ext' # full path
                         ]
        for it in minifiedFiles:
            self.assertTrue(minify.isMinified(it), it + ' IS NOT a minified file.')

        for it in unminifiedFiles:
            self.assertFalse(minify.isMinified(it), it + ' IS a minified file.')

    def testNominify(self):
        minify.NO_MINIFY_FILES = ['abc.css', '*123*.css', '?456?.css', '*/jquery*.js']
        # exact file name matches
        self.assertTrue(minify.nominify('abc.css'))

        # wildcards
        self.assertTrue(minify.nominify('abc123.css'))
        self.assertTrue(minify.nominify('123abc.css'))
        self.assertTrue(minify.nominify('abc123abc.css'))
        self.assertTrue(minify.nominify('a456b.css'))

        # filename with wildcard characters
        self.assertTrue(minify.nominify('*123.css'))
        self.assertTrue(minify.nominify('123*.css'))
        self.assertTrue(minify.nominify('*123*.css'))
        self.assertTrue(minify.nominify('?123.css'))
        self.assertTrue(minify.nominify('123?.css'))
        self.assertTrue(minify.nominify('?123?.css'))
        self.assertTrue(minify.nominify('/a/b/c/jquery.js'))
        self.assertTrue(minify.nominify('/a/b/c/jquery-1.9.1.js'))
        self.assertTrue(minify.nominify(r'c:\a\b\c\jquery-1.9.1.js'))

        ### full path
        # exact file name matches
        self.assertTrue(minify.nominify(r'c:\a\b\c\abc.css'))
        self.assertTrue(minify.nominify('/a/b/c/abc.css'))

        # wildcards
        self.assertTrue(minify.nominify(r'c:\a\b\c\abc123.css'))
        self.assertTrue(minify.nominify(r'c:\a\b\c\123abc.css'))
        self.assertTrue(minify.nominify(r'c:\a\b\c\abc123abc.css'))
        self.assertTrue(minify.nominify(r'c:\a\b\c\a456b.css'))
        self.assertTrue(minify.nominify(r'c:\a\b\c\*456*.css'))
        self.assertTrue(minify.nominify(r'c:\a\b\c\?456?.css'))

        # filename with wildcard characters
        self.assertTrue(minify.nominify(r'c:\a\b\c\*123.css'))
        self.assertTrue(minify.nominify(r'c:\a\b\c\123*.css'))
        self.assertTrue(minify.nominify(r'c:\a\b\c\*123*.css'))

    def testNoupdate(self):
        minify.NO_UPDATE_FILES = ['abc.css', '*123*.css', '?456?.css', '*/jquery*.js']
        # exact file name matches
        self.assertTrue(minify.noupdate('abc.css'))

        # wildcards
        self.assertTrue(minify.noupdate('abc123.css'))
        self.assertTrue(minify.noupdate('123abc.css'))
        self.assertTrue(minify.noupdate('abc123abc.css'))
        self.assertTrue(minify.noupdate('a456b.css'))

        # filename with wildcard characters
        self.assertTrue(minify.noupdate('*123.css'))
        self.assertTrue(minify.noupdate('123*.css'))
        self.assertTrue(minify.noupdate('*123*.css'))
        self.assertTrue(minify.noupdate('?123.css'))
        self.assertTrue(minify.noupdate('123?.css'))
        self.assertTrue(minify.noupdate('?123?.css'))
        self.assertTrue(minify.noupdate('/a/b/c/jquery.js'))
        self.assertTrue(minify.noupdate('/a/b/c/jquery-1.9.1.js'))
        self.assertTrue(minify.noupdate(r'c:\a\b\c\jquery-1.9.1.js'))

        ### full path
        # exact file name matches
        self.assertTrue(minify.noupdate(r'c:\a\b\c\abc.css'))
        self.assertTrue(minify.noupdate('/a/b/c/abc.css'))

        # wildcards
        self.assertTrue(minify.noupdate(r'c:\a\b\c\abc123.css'))
        self.assertTrue(minify.noupdate(r'c:\a\b\c\123abc.css'))
        self.assertTrue(minify.noupdate(r'c:\a\b\c\abc123abc.css'))
        self.assertTrue(minify.noupdate(r'c:\a\b\c\a456b.css'))
        self.assertTrue(minify.noupdate(r'c:\a\b\c\*456*.css'))
        self.assertTrue(minify.noupdate(r'c:\a\b\c\?456?.css'))

        # filename with wildcard characters
        self.assertTrue(minify.noupdate(r'c:\a\b\c\*123.css'))
        self.assertTrue(minify.noupdate(r'c:\a\b\c\123*.css'))
        self.assertTrue(minify.noupdate(r'c:\a\b\c\*123*.css'))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()