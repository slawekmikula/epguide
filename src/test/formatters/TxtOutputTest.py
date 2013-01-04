# -*- coding: utf-8 -*-
import unittest

from epguide.data_formats import Channel
from epguide.data_formats import Event
import datetime
from epguide.formatters import TxtOutput
import StringIO

class  TxtOutputTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testChannel(self):
        channel = Channel('TVP 1', "TVP-1")
        otherChannel = Channel('TVP 2', "TVP-2")

        f = StringIO.StringIO()
        output = TxtOutput.TxtOutput()
        output.Init(f)
        channel_list = [channel, otherChannel]
        output.SaveChannelList(channel_list)
        output.Finish()
        expected="""
TVP-1 - TVP 1
TVP-2 - TVP 2
""".lstrip()
        self.assertEqual(f.getvalue(), expected)


    def testEvent(self):
        event = Event(123, 'testchan', 'simple event', 'subtitle for an event',
            'movie', 'this is description for an event',
            datetime.date.today(),
            datetime.date.today() + datetime.timedelta(days=1))

        f = StringIO.StringIO()
        output = TxtOutput.TxtOutput()
        output.Init(f)
        guide = [event]
        day = datetime.datetime(2012, 12, 31)
        output.SaveGuide(day, guide)
        output.Finish()
        expected="""
Program testchan na dzien: 2012-12-31
--------------------------------------------

 00:00 00:00   simple event
             this is description for an event
"""
        self.assertEqual(f.getvalue(), expected)

if __name__ == '__main__':
    unittest.main()

