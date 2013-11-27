# -*- coding: utf-8 -*-
import unittest
from epguide.data_formats import Event, Imdb, ParentalRating, ParserOptions, Channel
from epguide.parsers.teleman.TelemanData import TelemanEventDetails, TelemanEvent

class  MovieWithOriginalTitleTest(unittest.TestCase):
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

        primary_title = 'Liberator 2'
        secondary_title = ''
        description = u"description"
        original_title = u"original title"
        year = u"2009"
        country = u"USA"
        genre = u"FILM GANGSTERSKI"
        pg = ParentalRating(u"od 16 lat", 16)
        details = TelemanEventDetails(primary_title, secondary_title, description, original_title, year, country, genre, imdb, filmweb, photo_url, pg)
        
        title = 'Megahit: Liberator 2'
        main_category = 'Movie/Drama'
        category = 'film sensacyjny, USA 1995'
        desc = 'summary'
        time_start = '2013-01-02 02:10:00'
        time_end = '2013-01-02 03:50:00'
        url = None

        parser_options = ParserOptions(split_title = True, add_original_title_to_title = True, add_year_to_title = True, add_age_rating_to_title = 16)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u"original title (2009) - Liberator 2 [od 16 lat] [Megahit]")
        self.assertEqual(event.get_filename(), u"original title (2009) - Liberator 2 [od 16 lat] [Megahit]")

        parser_options = ParserOptions(split_title = True, add_original_title_to_title = False, add_year_to_title = True, add_age_rating_to_title = 16)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), "Liberator 2 [od 16 lat] [Megahit]")
        self.assertEqual(event.get_filename(), u"Liberator 2 [od 16 lat] [Megahit]")

        parser_options = ParserOptions(split_title = True, add_original_title_to_title = True, add_year_to_title = False, add_age_rating_to_title = 16)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u"original title - Liberator 2 [od 16 lat] [Megahit]")
        self.assertEqual(event.get_filename(), u"original title - Liberator 2 [od 16 lat] [Megahit]")

        parser_options = ParserOptions(split_title = True, add_original_title_to_title = False, add_year_to_title = False, add_age_rating_to_title = 16)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), "Liberator 2 [od 16 lat] [Megahit]")
        self.assertEqual(event.get_filename(), u"Liberator 2 [od 16 lat] [Megahit]")


        parser_options = ParserOptions(split_title = True, add_original_title_to_title = True, add_year_to_title = True, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u"original title (2009) - Liberator 2 [Megahit]")
        self.assertEqual(event.get_filename(), u"original title (2009) - Liberator 2 [Megahit]")

        parser_options = ParserOptions(split_title = True, add_original_title_to_title = False, add_year_to_title = True, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), "Liberator 2 [Megahit]")
        self.assertEqual(event.get_filename(), u"Liberator 2 [Megahit]")

        parser_options = ParserOptions(split_title = True, add_original_title_to_title = True, add_year_to_title = False, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u"original title - Liberator 2 [Megahit]")
        self.assertEqual(event.get_filename(), u"original title - Liberator 2 [Megahit]")

        parser_options = ParserOptions(split_title = True, add_original_title_to_title = False, add_year_to_title = False, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), "Liberator 2 [Megahit]")
        self.assertEqual(event.get_filename(), u"Liberator 2 [Megahit]")


        parser_options = ParserOptions(split_title = True, add_original_title_to_title = False, add_year_to_title = False, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_description(), u'summarydescription\nTytul oryginalny:original title')




if __name__ == '__main__':
    unittest.main()

