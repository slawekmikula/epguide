# -*- coding: utf-8 -*-
import unittest
from epguide.common import Config
from epguide.epguide import EpGuide
import datetime

class  GetDailyProgrammeTestCase(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.config.options
#epguide -c TTV -w -f xmltv -o ~/.xmltv/tv_grab_file.xmltv --verbose
        args = ['-c', 'TVP-2', '-t', '-f','xmltv', '-o', 'tv_grab_file.xmltv','--verbose']
        
        self.config.ParseCommandLine(args)

        self.epguide = EpGuide(self.config)
    

#    def tearDown(self):
#        self.epguide.dispose()
#        self.epguide = None

    def test_epgguide(self):
        #assert x != y;
        #self.assertEqual(x, y, "Msg");
        self.epguide.parser.Init()
        programmes = self.epguide.parser.get_guide(datetime.datetime.today(), "TVP-2")
        self.assertGreater(programmes.count, 0, "Expected programmes")
        print "programmes: "+ str(programmes)
#        self.fail("TODO: Write test")

if __name__ == '__main__':
    unittest.main()

