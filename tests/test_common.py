# tests for common classes

import unittest

class ConfigTest(unittest.TestCase):
    """
    test for commandline parsing
    """
    
    def setUp(self):
        pass
    
    def testCmdParser(self):
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

if __name__ == '__main__':
    unittest.main()