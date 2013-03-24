# -*- coding: utf-8 -*-
import unittest

from epguide.data_formats import Channel
from epguide.data_formats import Event
import datetime
from epguide.formatters import XmltvOutput
import StringIO

class  XmltvOutputTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testChannel(self):
        channel = Channel('TVP 1', "TVP-1")
        otherChannel = Channel('TVP 2', "TVP-2")

        f = StringIO.StringIO()
        output = XmltvOutput.XmltvOutput()
        output.Init(f)
        channel_list = [channel, otherChannel]
        output.SaveChannelList(channel_list)
        output.Finish()
        expected="""
<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE tv SYSTEM "xmltv.dtd">
<tv generator-info-name="epguide generator">
  <channel id="TVP-1"><display-name lang="pl">TVP 1</display-name></channel>
  <channel id="TVP-2"><display-name lang="pl">TVP 2</display-name></channel>
</tv>
""".lstrip()
        self.assertEqual(f.getvalue(), expected)


    def testEventFull(self):
        day = datetime.datetime(2012, 12, 31)
        event = Event(123, 'testchan', 'simple event', 'subtitle for an event',
            'movie', 'this is description for an event',
            day,
            day + datetime.timedelta(days=1),
            "2/3")

        f = StringIO.StringIO()
        output = XmltvOutput.XmltvOutput()
        output.Init(f)
        guide = [event]
        output.SaveGuide(day, guide)
        output.SaveGuideChannels()
        output.Finish()
        expected="""
<tv generator-info-name="epguide generator">
  <programme start="20121231000000 +0100" stop="20130101000000 +0100" channel="123">
    <title>simple event</title>
    <sub-title>subtitle for an event</sub-title>
    <desc>this is description for an event</desc>
    <category>movie</category>
    <episode-num system="onscreen">2/3</episode-num>
  </programme>
  <channel id="123"><display-name lang="pl">testchan</display-name></channel>
</tv>
""".lstrip()
        self.assertEqual(f.getvalue(), expected)
        
    def testEventMinimal(self):
        day = datetime.datetime(2012, 12, 31)
        event = Event(123, 'testchan', 'simple event', None,
            'movie', None,
            day,
            day + datetime.timedelta(days=1),
            None)

        f = StringIO.StringIO()
        output = XmltvOutput.XmltvOutput()
        output.Init(f)
        guide = [event]
        output.SaveGuide(day, guide)
        output.SaveGuideChannels()
        output.Finish()
        expected="""
<tv generator-info-name="epguide generator">
  <programme start="20121231000000 +0100" stop="20130101000000 +0100" channel="123">
    <title>simple event</title>
    <category>movie</category>
  </programme>
  <channel id="123"><display-name lang="pl">testchan</display-name></channel>
</tv>
""".lstrip()
        self.assertEqual(f.getvalue(), expected)

if __name__ == '__main__':
    unittest.main()

