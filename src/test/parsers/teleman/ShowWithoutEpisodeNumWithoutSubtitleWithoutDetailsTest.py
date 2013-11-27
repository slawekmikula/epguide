# -*- coding: utf-8 -*-
import unittest
from epguide.data_formats import Event, Imdb, ParentalRating, ParserOptions, Channel
from epguide.parsers.teleman.TelemanData import TelemanEventDetails, TelemanEvent

class  ShowWithoutEpisodeNumWithoutSubtitleWithoutDetailsTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        pass

    def tearDown(self):
        pass


    def testShowWithoutEpisodeNumWithoutSubtitleWithoutDetails(self):
        channel = Channel('x','x',"x")

        title = u'Uwaga'
        category = 'magazyn reporterów'
        desc = 'One line summary.'
        
        main_category = 'Show/Game show'
        time_start = '2013-01-02 02:10:00'
        time_end = '2013-01-02 03:50:00'
        url = None

        parser_options = ParserOptions(split_title = False, add_original_title_to_title = True, add_year_to_title = True, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Uwaga') # with original title and year
        
         
        parser_options = ParserOptions(split_title = False, add_original_title_to_title = False, add_year_to_title = True, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Uwaga') # with year 

        
        parser_options = ParserOptions(split_title = False, add_original_title_to_title = True, add_year_to_title = False, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Uwaga') # with original title 

        parser_options = ParserOptions(split_title = False, add_original_title_to_title = False, add_year_to_title = False, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Uwaga')# nothing


        parser_options = ParserOptions(split_title = False, add_original_title_to_title = True, add_year_to_title = True, add_age_rating_to_title = 12)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Uwaga')# with original title, year and age

        parser_options = ParserOptions(split_title = False, add_original_title_to_title = False, add_year_to_title = True, add_age_rating_to_title = 12)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Uwaga')# with year and age

        parser_options = ParserOptions(split_title = False, add_original_title_to_title = True, add_year_to_title = False, add_age_rating_to_title = 12)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Uwaga') # with original title and age

        parser_options = ParserOptions(split_title = False, add_original_title_to_title = False, add_year_to_title = False, add_age_rating_to_title = 12)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Uwaga') # with age

        
        self.assertEqual(event.get_subtitle(), None)
        self.assertEqual(event.get_description(), "One line summary.")
        
        
if __name__ == '__main__':
    unittest.main()

