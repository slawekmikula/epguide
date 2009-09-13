# test for output classes

import unittest

class XmlOutputTest(unittest.TestCase):
    """
    test for xmltv output format
    """
    
    def setUp(self):
        pass
    
    def testParser(self):
        from common import Config
        
        config = Config()
        config.ParseCommandLine('')
        self.assertEqual(config.options.output, '')
    
    def testReadConfig(self):
        pass
    
    def testPrintHelp(self):
        pass
    
    def testPrintLicence(self):
        pass

class TxtOutputTest(unittest.TestCase):
    """
    test for txt output
    """
    
    def setUp(self):
        pass

if __name__ == '__main__':
    unittest.main()