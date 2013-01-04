# -*- coding: utf-8 -*-
import unittest
from epguide.common import Config
from epguide.epguide import EpGuide

class  EpgguideTestCase(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.config.options
#epguide -c TTV -w -f xmltv -o ~/.xmltv/tv_grab_file.xmltv --verbose
        args = ['-c', 'TTV', '-t', '-f','xmltv', '-o', 'tv_grab_file.xmltv','--verbose']
        
        self.config.ParseCommandLine(args)

        self.epguide = EpGuide(self.config)
    

#    def tearDown(self):
#        self.epguide.dispose()
#        self.epguide = None

    def test_epgguide(self):
        #assert x != y;
        #self.assertEqual(x, y, "Msg");
        self.epguide.Execute()
#        self.fail("TODO: Write test")

if __name__ == '__main__':
    unittest.main()

