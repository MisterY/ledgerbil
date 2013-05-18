#!/usr/bin/python

"""unit test for ledgerfile.py"""

__author__ = 'scarpent'
__license__ = 'gpl v3 or greater'
__email__ = 'scottc@movingtofreedom.org'


import unittest
import inspect
from shutil import copyfile
from os import remove

import ledgerfile
from redirector import Redirector

testdir = 'tests/files/'
testfile = testdir + 'test.ledger'
testfile_copy = testdir + 'test.ledger.copy'
sortedfile = testdir + 'test-already-sorted.ledger'
alpha_unsortedfile = testdir + 'test-alpha-unsorted.ledger'
alpha_sortedfile = testdir + 'test-alpha-sorted.ledger'


def getTempFilename():
    # gets the name of the calling function
    return testdir + 'temp_' + inspect.stack()[1][3]


class LedgerFileInit(Redirector):

    def testBadFilename(self):
        """should fail with 'No such file or directory'"""
        expected = "error: [Errno 2] No such file or directory:"
        try:
            ledgerfile.LedgerFile('bad.filename')
        except SystemExit:
            pass

        self.redirecterr.seek(0)
        actual = self.redirecterr.read()
        self.assertTrue(expected in actual)

    def testParsedFileUnchangedViaPrint(self):
        """file output after parsing should be identical to input file"""
        f = open(testfile, 'r')
        expected = f.read()
        f.close()
        ldgfile = ledgerfile.LedgerFile(testfile)
        ldgfile.printFile()
        self.redirect.seek(0)
        self.assertEqual(expected, self.redirect.read())

    def testParsedFileUnchangedViaWrite(self):
        """file output after parsing should be identical to input file"""
        tempfile = getTempFilename()
        f = open(testfile, 'r')
        expected = f.read()
        f.close()
        copyfile(testfile, tempfile)
        ldgfile = ledgerfile.LedgerFile(tempfile)
        ldgfile.writeFile()
        f = open(tempfile, 'r')
        actual = f.read()
        f.close()
        remove(tempfile)
        self.assertEqual(expected, actual)

    def testCountInitialNonTransaction(self):
        """counts initial non-transaction (probably a comment)"""
        tempfile = getTempFilename()
        testdata = '''; blah
; blah blah blah
2013/05/06 payee name
    expenses: misc
    liabilities: credit card  $-50
'''
        f = open(tempfile, 'w')
        f.write(testdata)
        f.close()
        ldgfile = ledgerfile.LedgerFile(tempfile)
        remove(tempfile)
        self.assertEquals(2, ldgfile.thingCounter)

    def testCountInitialTransaction(self):
        """counts initial transaction"""
        tempfile = getTempFilename()
        testdata = '''2013/05/06 payee name
    expenses: misc
    liabilities: credit card  $-50
; blah blah blah
2013/05/06 payee name
    expenses: misc
    liabilities: credit card  $-50
'''
        f = open(tempfile, 'w')
        f.write(testdata)
        f.close()
        ldgfile = ledgerfile.LedgerFile(tempfile)
        remove(tempfile)
        self.assertEquals(2, ldgfile.thingCounter)


class Sorting(unittest.TestCase):

    def testAlreadySortedFileUnchanged(self):
        """file output after sorting is identical to sorted input file"""
        f = open(sortedfile, 'r')
        expected = f.read()
        f.close()
        tempfile = getTempFilename()
        copyfile(sortedfile, tempfile)
        ldgfile = ledgerfile.LedgerFile(tempfile)
        ldgfile.sort()
        ldgfile.writeFile()
        f = open(tempfile, 'r')
        actual = f.read()
        remove(tempfile)
        self.assertEqual(expected, actual)

    def testSorting(self):
        """test sorting"""
        f = open(alpha_sortedfile, 'r')
        expected = f.read()
        f.close()
        tempfile = getTempFilename()
        copyfile(alpha_unsortedfile, tempfile)
        ldgfile = ledgerfile.LedgerFile(tempfile)
        ldgfile.sort()
        ldgfile.writeFile()
        f = open(tempfile, 'r')
        actual = f.read()
        remove(tempfile)
        self.assertEqual(expected, actual)

class Misc(unittest.TestCase):

    def testGetThings(self):
        """retrieves data via getThings method"""
        tempfile = getTempFilename()
        # yes, the first line is an invalid date, making it not a transaction
        # - when testing just test_ledgerfile, contributes to 100% test on
        #   thing
        expected = '''2013/02/30 payee name
    expenses: misc
    liabilities: credit card  $-38
; blah blah blah
2013/05/06 payee name
    expenses: misc
    liabilities: credit card  $-50
2013/05/17  payee name
    expenses: misc
    liabilities: credit card  $-42
'''
        f = open(tempfile, 'w')
        f.write(expected)
        f.close()
        ldgfile = ledgerfile.LedgerFile(tempfile)
        things = ldgfile.getThings()
        f = open(tempfile, 'r+')
        for thing in things:
            for line in thing.getLines():
                f.write(line + '\n')
        f.seek(0)
        actual = f.read()
        f.close()
        remove(tempfile)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()         # pragma: no cover