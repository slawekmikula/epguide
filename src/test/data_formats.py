import unittest

from data_formats import Channel
from data_formats import Event

class  Data_formatsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testChannel(self):
        channel = Channel('testchannel', 123)
        self.assertEqual(channel.name, 'testchannel')
        self.assertEqual(channel.id, 123)
        otherChannel = Channel('testchan', 123)
        self.assertEqual(channel, otherChannel)

    def testEvent(self):
        event = Event(123, 'testchan', 'simple event', 'subtitle for an event',
            'movie', 'this is description for an event',
            datetime.date.today(),
            datetime.date.today() + datetime.timedelta(days=1))
        self.assertEqual(event.channel_id, 123)
        self.assertEqual(event.time_start, datetime.date.today())
        self.assertEqual(event.subtitle, 'subtitle for an event')

if __name__ == '__main__':
    unittest.main()

