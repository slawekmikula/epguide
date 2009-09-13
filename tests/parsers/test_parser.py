# test for input data

import unittest

class WpParserTest(unittest.TestCase):
    """
    test for parsing Wp.Pl provider data 
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
    
class CpParserTest(unittest.TestCase):
    """
    test for parsing Cyfra.Pl provider data 
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

if __name__ == '__main__':
    unittest.main()