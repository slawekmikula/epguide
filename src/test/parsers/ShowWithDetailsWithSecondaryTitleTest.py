# -*- coding: utf-8 -*-
from epguide.data_formats import Imdb, ParentalRating, ParserOptions, Channel
from epguide.parsers.teleman.TelemanData import TelemanEventDetails, TelemanEvent
import unittest

class  ShowWithDetailsWithSecondaryTitleTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        pass

    def tearDown(self):
        pass


    def testShowWithDetailsWithSecondaryTitle(self):
        imdb_url = u"x"
        imdb_rank = u"x"
        imdb = Imdb(imdb_url, imdb_rank)
        filmweb_url = u"x"
        filmweb_rank = u"x"
        filmweb = Imdb(filmweb_url, filmweb_rank)
        photo_url = u"x"
        channel = Channel('x', 'x', "x")

        title = u'Na dobre i na złe: Pierwszy dzień (518)'
        category = 'serial obyczajowy'
        desc = 'One line summary.'
        
        primary_title = u'Na dobre i na złe'
        secondary_title = u'odc. 518: Pierwszy dzień'
        original_title = None
        genre = u"serial obyczajowy"
        country = u"Polska"
        year = u"2013"
        pg = ParentalRating(u"od 12 lat", 12)
        description = u"Long description"
        details = TelemanEventDetails(primary_title, secondary_title, description, original_title, year, country, genre, imdb, filmweb, photo_url, pg)
        
        main_category = 'Show/Game show'
        time_start = '2013-01-02 02:10:00'
        time_end = '2013-01-02 03:50:00'
        url = None
        parser_options = ParserOptions(split_title=False, add_original_title_to_title=True, add_year_to_title=True, add_age_rating_to_title=18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u'Na dobre i na złe: Pierwszy dzień (518)')  
        self.assertEqual(event.get_subtitle(), None)
        self.assertEqual(event.get_episode_num(), None)

        parser_options = ParserOptions(split_title=True, add_original_title_to_title=True, add_year_to_title=True, add_age_rating_to_title=18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u'Na dobre i na złe (odc. 518) - Pierwszy dzień')  # with original title and year 
        self.assertEqual(event.get_subtitle(), u"Pierwszy dzień")
        self.assertEqual(event.get_episode_num(), "518")

        parser_options = ParserOptions(split_title=True, add_original_title_to_title=False, add_year_to_title=True, add_age_rating_to_title=18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u'Na dobre i na złe (odc. 518) - Pierwszy dzień')  # with year 
        self.assertEqual(event.get_subtitle(), u"Pierwszy dzień")
        self.assertEqual(event.get_episode_num(), "518")

        parser_options = ParserOptions(split_title=True, add_original_title_to_title=True, add_year_to_title=False, add_age_rating_to_title=18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u'Na dobre i na złe (odc. 518) - Pierwszy dzień')  # with original title 
        self.assertEqual(event.get_subtitle(), u"Pierwszy dzień")
        self.assertEqual(event.get_episode_num(), "518")

        parser_options = ParserOptions(split_title=True, add_original_title_to_title=False, add_year_to_title=False, add_age_rating_to_title=18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u'Na dobre i na złe (odc. 518) - Pierwszy dzień')  # nothing
        self.assertEqual(event.get_subtitle(), u"Pierwszy dzień")
        self.assertEqual(event.get_episode_num(), "518")


        parser_options = ParserOptions(split_title=True, add_original_title_to_title=True, add_year_to_title=True, add_age_rating_to_title=12)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u'Na dobre i na złe [od 12 lat] (odc. 518) - Pierwszy dzień')  # with original title, year and age
        self.assertEqual(event.get_subtitle(), u"Pierwszy dzień")
        self.assertEqual(event.get_episode_num(), "518")

        parser_options = ParserOptions(split_title=True, add_original_title_to_title=False, add_year_to_title=True, add_age_rating_to_title=12)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u'Na dobre i na złe [od 12 lat] (odc. 518) - Pierwszy dzień')  # with year and age
        self.assertEqual(event.get_subtitle(), u"Pierwszy dzień")
        self.assertEqual(event.get_episode_num(), "518")

        parser_options = ParserOptions(split_title=True, add_original_title_to_title=True, add_year_to_title=False, add_age_rating_to_title=12)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u'Na dobre i na złe [od 12 lat] (odc. 518) - Pierwszy dzień')  # with original title and age
        self.assertEqual(event.get_subtitle(), u"Pierwszy dzień")
        self.assertEqual(event.get_episode_num(), "518")

        parser_options = ParserOptions(split_title=True, add_original_title_to_title=False, add_year_to_title=False, add_age_rating_to_title=12)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u'Na dobre i na złe [od 12 lat] (odc. 518) - Pierwszy dzień')  # with age
        self.assertEqual(event.get_subtitle(), u"Pierwszy dzień")
        self.assertEqual(event.get_episode_num(), "518")

        self.assertEqual(event.get_description(), u'One line summary.Long description')


if __name__ == '__main__':
    unittest.main()

