# -*- coding: utf-8 -*-
import unittest

from epguide.data_formats import Event, Imdb, ParentalRating, ParserOptions, Channel
import datetime
from epguide.formatters import TxtOutput
import StringIO
from epguide.parsers.teleman.TelemanData import TelemanEventDetails, TelemanEvent

class  TxtOutputTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testChannel(self):
        channel = Channel('TVP-1', "TVP 1")
        otherChannel = Channel('TVP-2', "TVP 2")

        f = StringIO.StringIO()
        output = TxtOutput.TxtOutput()
        output.Init(f)
        channel_list = [channel, otherChannel]
        output.SaveChannelList(channel_list)
        output.Finish()
        expected = """
TVP-1 - TVP 1
TVP-2 - TVP 2
""".lstrip()
        self.assertEqual(f.getvalue(), expected)


    def testEvent(self):
        channel = Channel(123, 'testchan', 'http://media.teleman.pl/logos/m/tvp-1.png')
        parserOptions = ParserOptions()
        event = TelemanEvent(parserOptions, channel, 'simple event', 'Movie/Drama', 'movie',
                             'this is description for an event', datetime.date.today(), datetime.date.today() + datetime.timedelta(days=1),
                             None)

        f = StringIO.StringIO()
        output = TxtOutput.TxtOutput()
        output.Init(f)
        guide = [event]
        day = datetime.datetime(2012, 12, 31)
        output.SaveGuide(day, guide)
        output.Finish()
        expected = u"""
Program testchan na dzień: 2012-12-31
--------------------------------------------

 00:00 00:00 simple event |  |  | Movie/Drama
             this is description for an event
"""
        actual = f.getvalue()
        print("actual: " + actual)
        print("expected: " + expected)
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()

