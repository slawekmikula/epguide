# -*- coding: utf-8 -*-
import unittest

from epguide.data_formats import Channel

class DataFormatsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testChannel(self):
        channel = Channel(123, 'testchannel')
        self.assertEqual(channel.name, 'testchannel')
        self.assertEqual(channel.id, 123)
        otherChannel = Channel(123, 'testchan')
        self.assertEqual(channel, otherChannel)

if __name__ == '__main__':
    unittest.main()

