# -*- coding: utf-8 -*-
import unittest
from epguide.data_formats import Event, Imdb, ParentalRating, ParserOptions, Channel
from epguide.parsers.teleman.TelemanData import TelemanEventDetails, TelemanEvent

class  SplitTitleTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        pass

    def tearDown(self):
        pass


    def testShow3(self):
        imdb_url = u"x"
        imdb_rank = u"x"
        imdb = Imdb(imdb_url, imdb_rank)
        filmweb_url = u"x"
        filmweb_rank = u"x"
        filmweb = Imdb(filmweb_url, filmweb_rank)
        photo_url = u"x"
        channel = Channel('x','x',"x")

        title = u'Na linii strzału 2 (15)'
        category = 'serial sensacyjny'
        desc = 'One line summary.'
        
        primary_title = 'Na linii strzału'
        secondary_title = 'sezon 2 odc. 15'
        original_title = "In Plain Sight: In My Humboldt Opinion"
        genre = u"serial sensacyjny"
        country = u"USA"
        year = u"2009"
        pg = ParentalRating(u"od 16 lat", 16)
        description = u"Long description"
        details = TelemanEventDetails(primary_title, secondary_title, description, original_title, year, country, genre, imdb, filmweb, photo_url, pg)
        
        main_category = 'Show/Game show'
        time_start = '2013-01-02 02:10:00'
        time_end = '2013-01-02 03:50:00'
        url = None
        parser_options = ParserOptions(split_title = False, add_original_title_to_title = True, add_year_to_title = True, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u'In Plain Sight: In My Humboldt Opinion - Na linii strza\u0142u 2 (15)') # with original title and year 

        parser_options = ParserOptions(split_title = False, add_original_title_to_title = False, add_year_to_title = True, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u'Na linii strza\u0142u 2 (15)') # with year 

        parser_options = ParserOptions(split_title = False, add_original_title_to_title = True, add_year_to_title = False, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u'In Plain Sight: In My Humboldt Opinion - Na linii strzału 2 (15)') # with original title 

        parser_options = ParserOptions(split_title = False, add_original_title_to_title = False, add_year_to_title = False, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u'Na linii strzału 2 (15)')# nothing


        parser_options = ParserOptions(split_title = False, add_original_title_to_title = True, add_year_to_title = True, add_age_rating_to_title = 12)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u'In Plain Sight: In My Humboldt Opinion - Na linii strzału 2 (15) [od 16 lat]')# with original title, year and age

        parser_options = ParserOptions(split_title = False, add_original_title_to_title = False, add_year_to_title = True, add_age_rating_to_title = 12)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u'Na linii strzału 2 (15) [od 16 lat]')# with year and age

        parser_options = ParserOptions(split_title = False, add_original_title_to_title = True, add_year_to_title = False, add_age_rating_to_title = 12)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u'In Plain Sight: In My Humboldt Opinion - Na linii strzału 2 (15) [od 16 lat]') # with original title and age

        parser_options = ParserOptions(split_title = False, add_original_title_to_title = False, add_year_to_title = False, add_age_rating_to_title = 12)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_title(), u'Na linii strzału 2 (15) [od 16 lat]') # with age


        parser_options = ParserOptions(split_title = False, add_original_title_to_title = False, add_year_to_title = False, add_age_rating_to_title = 18)
        event = TelemanEvent(parser_options, channel, title, main_category, category, desc, time_start, time_end, url, details=details)
        self.assertEqual(event.get_subtitle(), None)
        self.assertEqual(event.get_description(), "One line summary.Long description\nTytul oryginalny:In Plain Sight: In My Humboldt Opinion")



if __name__ == '__main__':
    unittest.main()

