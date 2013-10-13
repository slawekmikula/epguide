# -*- coding: utf-8 -*-
import unittest
from epguide.data_formats import Event, Imdb, ParentalRating, ParserOptions, Channel
from epguide.parsers.teleman.TelemanData import TelemanEventDetails, TelemanEvent

class  MovieWithoutOriginalTitleTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        pass

    def tearDown(self):
        pass



    def testMovie(self):
        imdb_url = u"x"
        imdb_rank = u"x"
        imdb = Imdb(imdb_url, imdb_rank)
        filmweb_url = u"x"
        filmweb_rank = u"x"
        filmweb = Imdb(filmweb_url, filmweb_rank)
        photo_url = u"x"
        channel = Channel('x', 'x', "x")

        primary_title = 'U Pana Boga za piecem'
        secondary_title = ""
        description = u"description"
        original_title = ""
        year = u"1998"
        country = u"Polska"
        genre = u"KOMEDIA"
        pg = ParentalRating(u"od 16 lat", 16)
        details = TelemanEventDetails(primary_title, secondary_title, description, original_title, year, country, genre, imdb, filmweb, photo_url, pg)
        
        title = 'Wakacyjny hit Jedynki: U Pana Boga za piecem'
        main_category = 'Movie/Drama'
        category = 'komedia, Polska 1998'
        desc = 'summary'
        time_start = '2013-01-02 02:10:00'
        time_end = '2013-01-02 03:50:00'
        url = None

        parser_options = ParserOptions(split_title = False, add_original_title_to_title = False, add_year_to_title = False, add_age_rating_to_title = 99)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u"Wakacyjny hit Jedynki: U Pana Boga za piecem")

        parser_options = ParserOptions(split_title = False, add_original_title_to_title = True, add_year_to_title = True, add_age_rating_to_title = 16)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u"Wakacyjny hit Jedynki: U Pana Boga za piecem (1998) [od 16 lat]")

        parser_options = ParserOptions(split_title = True, add_original_title_to_title = True, add_year_to_title = True, add_age_rating_to_title = 16)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u"U Pana Boga za piecem (Wakacyjny hit Jedynki) (1998) [od 16 lat]")

        parser_options = ParserOptions(split_title = True, add_original_title_to_title = False, add_year_to_title = True, add_age_rating_to_title = 16)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u"U Pana Boga za piecem (Wakacyjny hit Jedynki) (1998) [od 16 lat]")

        parser_options = ParserOptions(split_title = True, add_original_title_to_title = True, add_year_to_title = False, add_age_rating_to_title = 16)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u"U Pana Boga za piecem (Wakacyjny hit Jedynki) [od 16 lat]")

        parser_options = ParserOptions(split_title = True, add_original_title_to_title = False, add_year_to_title = False, add_age_rating_to_title = 16)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), "U Pana Boga za piecem (Wakacyjny hit Jedynki) [od 16 lat]")


        parser_options = ParserOptions(split_title = True, add_original_title_to_title = True, add_year_to_title = True, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u"U Pana Boga za piecem (Wakacyjny hit Jedynki) (1998)")

        parser_options = ParserOptions(split_title = True, add_original_title_to_title = False, add_year_to_title = True, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), "U Pana Boga za piecem (Wakacyjny hit Jedynki) (1998)")

        parser_options = ParserOptions(split_title = True, add_original_title_to_title = True, add_year_to_title = False, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u"U Pana Boga za piecem (Wakacyjny hit Jedynki)")

        parser_options = ParserOptions(split_title = True, add_original_title_to_title = False, add_year_to_title = False, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), "U Pana Boga za piecem (Wakacyjny hit Jedynki)")


        parser_options = ParserOptions(split_title = True, add_original_title_to_title = False, add_year_to_title = False, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_description(), u'summarydescription')




if __name__ == '__main__':
    unittest.main()

