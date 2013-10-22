# -*- coding: utf-8 -*-
import unittest
from epguide.data_formats import Event, Imdb, ParentalRating, ParserOptions, Channel
from epguide.parsers.teleman.TelemanData import TelemanEventDetails, TelemanEvent

class  ShowWithEpisodeNumWithoutSubtitleWithoutDetailsTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        pass

    def tearDown(self):
        pass


    def testShowWithEpisodeNumWithoutSubtitleWithoutDetails(self):
        channel = Channel('x','x',"x")

        title = u'Barwy szczęścia (948)'
        category = 'serial obyczajowy'
        desc = 'One line summary.'
        
        main_category = 'Show/Game show'
        time_start = '2013-01-02 02:10:00'
        time_end = '2013-01-02 03:50:00'
        url = None

        parser_options = ParserOptions(split_title = False, add_original_title_to_title = True, add_year_to_title = True, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Barwy szczęścia (948)') # with original title and year
        self.assertEqual(event.get_subtitle(), None)
        self.assertEqual(event.get_episode_num(), None)
        self.assertEqual(event.get_filename(), u'Barwy szczęścia (948)')
        
         
        parser_options = ParserOptions(split_title = False, add_original_title_to_title = False, add_year_to_title = True, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Barwy szczęścia (948)') # with year 
        self.assertEqual(event.get_subtitle(), None)
        self.assertEqual(event.get_episode_num(), None)
        self.assertEqual(event.get_filename(), u'Barwy szczęścia (948)')

        
        parser_options = ParserOptions(split_title = False, add_original_title_to_title = True, add_year_to_title = False, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Barwy szczęścia (948)') # with original title 
        self.assertEqual(event.get_subtitle(), None)
        self.assertEqual(event.get_episode_num(), None)
        self.assertEqual(event.get_filename(), u'Barwy szczęścia (948)')

        parser_options = ParserOptions(split_title = False, add_original_title_to_title = False, add_year_to_title = False, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Barwy szczęścia (948)')# nothing
        self.assertEqual(event.get_subtitle(), None)
        self.assertEqual(event.get_episode_num(), None)
        self.assertEqual(event.get_filename(), u'Barwy szczęścia (948)')


        parser_options = ParserOptions(split_title = False, add_original_title_to_title = True, add_year_to_title = True, add_age_rating_to_title = 12)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Barwy szczęścia (948)')# with original title, year and age
        self.assertEqual(event.get_subtitle(), None)
        self.assertEqual(event.get_episode_num(), None)
        self.assertEqual(event.get_filename(), u'Barwy szczęścia (948)')

        parser_options = ParserOptions(split_title = False, add_original_title_to_title = False, add_year_to_title = True, add_age_rating_to_title = 12)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Barwy szczęścia (948)')# with year and age
        self.assertEqual(event.get_subtitle(), None)
        self.assertEqual(event.get_episode_num(), None)
        self.assertEqual(event.get_filename(), u'Barwy szczęścia (948)')

        parser_options = ParserOptions(split_title = False, add_original_title_to_title = True, add_year_to_title = False, add_age_rating_to_title = 12)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Barwy szczęścia (948)') # with original title and age
        self.assertEqual(event.get_subtitle(), None)
        self.assertEqual(event.get_episode_num(), None)
        self.assertEqual(event.get_filename(), u'Barwy szczęścia (948)')

        parser_options = ParserOptions(split_title = False, add_original_title_to_title = False, add_year_to_title = False, add_age_rating_to_title = 12)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Barwy szczęścia (948)') # with age
        self.assertEqual(event.get_subtitle(), None)
        self.assertEqual(event.get_episode_num(), None)
        self.assertEqual(event.get_filename(), u'Barwy szczęścia (948)')




        parser_options = ParserOptions(split_title = True, add_original_title_to_title = True, add_year_to_title = True, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Barwy szczęścia') # with original title and year
        self.assertEqual(event.get_subtitle(), None)
        self.assertEqual(event.get_episode_num(), "948")
        self.assertEqual(event.get_filename(), u'Barwy szczęścia (948)')
        
         
        parser_options = ParserOptions(split_title = True, add_original_title_to_title = False, add_year_to_title = True, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Barwy szczęścia') # with year 
        self.assertEqual(event.get_subtitle(), None)
        self.assertEqual(event.get_episode_num(), "948")
        self.assertEqual(event.get_filename(), u'Barwy szczęścia (948)')

        
        parser_options = ParserOptions(split_title = True, add_original_title_to_title = True, add_year_to_title = False, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Barwy szczęścia') # with original title 
        self.assertEqual(event.get_subtitle(), None)
        self.assertEqual(event.get_episode_num(), "948")
        self.assertEqual(event.get_filename(), u'Barwy szczęścia (948)')

        parser_options = ParserOptions(split_title = True, add_original_title_to_title = False, add_year_to_title = False, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Barwy szczęścia')# nothing
        self.assertEqual(event.get_subtitle(), None)
        self.assertEqual(event.get_episode_num(), "948")
        self.assertEqual(event.get_filename(), u'Barwy szczęścia (948)')


        parser_options = ParserOptions(split_title = True, add_original_title_to_title = True, add_year_to_title = True, add_age_rating_to_title = 12)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Barwy szczęścia')# with original title, year and age
        self.assertEqual(event.get_subtitle(), None)
        self.assertEqual(event.get_episode_num(), "948")
        self.assertEqual(event.get_filename(), u'Barwy szczęścia (948)')

        parser_options = ParserOptions(split_title = True, add_original_title_to_title = False, add_year_to_title = True, add_age_rating_to_title = 12)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Barwy szczęścia')# with year and age
        self.assertEqual(event.get_subtitle(), None)
        self.assertEqual(event.get_episode_num(), "948")
        self.assertEqual(event.get_filename(), u'Barwy szczęścia (948)')

        parser_options = ParserOptions(split_title = True, add_original_title_to_title = True, add_year_to_title = False, add_age_rating_to_title = 12)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Barwy szczęścia') # with original title and age
        self.assertEqual(event.get_subtitle(), None)
        self.assertEqual(event.get_episode_num(), "948")
        self.assertEqual(event.get_filename(), u'Barwy szczęścia (948)')

        parser_options = ParserOptions(split_title = True, add_original_title_to_title = False, add_year_to_title = False, add_age_rating_to_title = 12)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=None)
        self.assertEqual(event.get_title(), u'Barwy szczęścia') # with age
        self.assertEqual(event.get_subtitle(), None)
        self.assertEqual(event.get_episode_num(), "948")
        self.assertEqual(event.get_filename(), u'Barwy szczęścia (948)')

        
        self.assertEqual(event.get_subtitle(), None)
        self.assertEqual(event.get_description(), "One line summary.")


if __name__ == '__main__':
    unittest.main()

