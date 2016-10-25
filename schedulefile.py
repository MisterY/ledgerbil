#!/usr/bin/env python

"""schedule file"""

from __future__ import print_function

from ledgerfile import LedgerFile
from schedulething import ScheduleThing


__author__ = 'Scott Carpenter'
__license__ = 'gpl v3 or greater'
__email__ = 'scottc@movingtofreedom.org'


class ScheduleFile(LedgerFile):

    def _add_thing_lines(self, lines):
        if lines:
            thing = ScheduleThing(lines)
            self.add_thing(thing)
