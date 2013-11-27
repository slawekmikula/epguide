# -*- coding: utf-8 -*-
import unittest
from epguide.data_formats import  ParserOptions, Channel
from epguide.parsers.teleman.TelemanData import TelemanEvent

class  ShowWithEpisodeNumWithSubtitleWithoutDetailsTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        pass

    def tearDown(self):
        pass


    def testShowWithEpisodeNumWithSubtitleWithoutDetails(self):
        channel = Channel('x', 'x', "x")

        title = u'Rodzinka.pl: Zachcianki (80)'
        category = 'serial komediowy'
        desc = 'One line summary.'
        
        main_category = 'Show/Game show'
        time_start = '2013-01-02 02:10:00'
        time_end = '2013-01-02 03:50:00'
        url = None

        parser_options = ParserOptions(split_title=False, add_original_title_to_title=True, add_year_to_title=True, add_age_rating_to_title=18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Rodzinka.pl: Zachcianki (80)') 
        self.assertEqual(event.get_subtitle(), None)
        self.assertEqual(event.get_episode_num(), None)
        self.assertEqual(event.get_filename(), u'Rodzinka.pl: Zachcianki (80)') 
        
        parser_options = ParserOptions(split_title=True, add_original_title_to_title=True, add_year_to_title=True, add_age_rating_to_title=18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Rodzinka.pl')  # with original title and year
        self.assertEqual(event.get_subtitle(), "Zachcianki")
        self.assertEqual(event.get_episode_num(), "80")
        self.assertEqual(event.get_filename(), u'Rodzinka.pl (80) Zachcianki') 
        
         
        parser_options = ParserOptions(split_title=True, add_original_title_to_title=False, add_year_to_title=True, add_age_rating_to_title=18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Rodzinka.pl')  # with year 
        self.assertEqual(event.get_subtitle(), "Zachcianki")
        self.assertEqual(event.get_episode_num(), "80")
        self.assertEqual(event.get_filename(), u'Rodzinka.pl (80) Zachcianki') 
        
        parser_options = ParserOptions(split_title=True, add_original_title_to_title=True, add_year_to_title=False, add_age_rating_to_title=18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Rodzinka.pl')  # with original title 
        self.assertEqual(event.get_subtitle(), "Zachcianki")
        self.assertEqual(event.get_episode_num(), "80")
        self.assertEqual(event.get_filename(), u'Rodzinka.pl (80) Zachcianki') 

        parser_options = ParserOptions(split_title=True, add_original_title_to_title=False, add_year_to_title=False, add_age_rating_to_title=18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Rodzinka.pl')  # nothing
        self.assertEqual(event.get_subtitle(), "Zachcianki")
        self.assertEqual(event.get_episode_num(), "80")
        self.assertEqual(event.get_filename(), u'Rodzinka.pl (80) Zachcianki') 


        parser_options = ParserOptions(split_title=True, add_original_title_to_title=True, add_year_to_title=True, add_age_rating_to_title=12)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Rodzinka.pl')  # with original title, year and age
        self.assertEqual(event.get_subtitle(), "Zachcianki")
        self.assertEqual(event.get_episode_num(), "80")
        self.assertEqual(event.get_filename(), u'Rodzinka.pl (80) Zachcianki') 

        parser_options = ParserOptions(split_title=True, add_original_title_to_title=False, add_year_to_title=True, add_age_rating_to_title=12)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Rodzinka.pl')  # with year and age
        self.assertEqual(event.get_subtitle(), "Zachcianki")
        self.assertEqual(event.get_episode_num(), "80")
        self.assertEqual(event.get_filename(), u'Rodzinka.pl (80) Zachcianki') 

        parser_options = ParserOptions(split_title=True, add_original_title_to_title=True, add_year_to_title=False, add_age_rating_to_title=12)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Rodzinka.pl')  # with original title and age
        self.assertEqual(event.get_subtitle(), "Zachcianki")
        self.assertEqual(event.get_episode_num(), "80")
        self.assertEqual(event.get_filename(), u'Rodzinka.pl (80) Zachcianki') 

        parser_options = ParserOptions(split_title=True, add_original_title_to_title=False, add_year_to_title=False, add_age_rating_to_title=12)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Rodzinka.pl')  # with age
        self.assertEqual(event.get_subtitle(), "Zachcianki")
        self.assertEqual(event.get_episode_num(), "80")
        self.assertEqual(event.get_filename(), u'Rodzinka.pl (80) Zachcianki') 

        self.assertEqual(event.get_description(), "One line summary.")

if __name__ == '__main__':
    unittest.main()

