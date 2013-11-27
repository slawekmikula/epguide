# -*- coding: utf-8 -*-
import unittest
import codecs
from epguide.parsers.gazeta import GazetaProgrammeDetailsParser
from epguide.parsers.gazeta.GazetaData import GazetaEventDetails, GazetaEvent
from epguide.data_formats import ParentalRating, ParserOptions, Channel
from epguide.util import to_string

class  GazetaProgrammeDetailsParserTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        pass

    def tearDown(self):
        pass

    def testGetDetails(self):
        p = GazetaProgrammeDetailsParser.GazetaProgrammeDetailsParser("a")
        f = codecs.open("Dziewczyna z Alabamy.html", "r", "ISO-8859-2")
        buf = f.read()
        actual = p.get_details(buf)        
        f.close()
        
        expected_description = u"\nOpis: Narzeczona syna pani burmistrz Nowego Jorku wraca przed ślubem na\n amerykańskie Południe, by uregulować sprawy, w tym? rozwód. Plus \nniezawodna Reese Witherspoon broniąca całość przed rutyną."
        expected_primary_title = u"Dziewczyna z Alabamy"
        expected_year = u"2002"
        expected_country = u"USA"
        expected_genre = u"Komedia romantyczna"
        expected_duration = u"1 godzina 44 minuty"
        expected_photo_url = u"Dziewczyna%20z%20Alabamy_pliki/d91d2a2effa1f879bb48d3b1aa9d58ec532d0800-thumb.jpg"
        expected_pg = ParentalRating(u"od12", 12)
        expected_crew = None
        expected = GazetaEventDetails(expected_primary_title, expected_description, expected_year, expected_country, expected_genre, expected_duration, expected_photo_url, expected_pg, expected_crew)

        print("actual  :"+to_string(actual))
        print("expected:"+to_string(expected))

        self.assertEqual(actual.description, expected.description)
        self.assertEqual(to_string(actual.pg), to_string(expected.pg))
        self.assertEqual(actual.photo_url, expected.photo_url)
        
        self.assertEqual(str(actual), str(expected))
        parserOptions = ParserOptions()
        channel = Channel('TVP-1', 'TVP 1')
        event = GazetaEvent(parserOptions, channel, 'Dziewczyna z Alabamy', \
                       'Movie/Drama', 'Komedia romantyczna', \
                       'Melanie jest nowojorską projektantką mody. Wkrótce ma poślubić bogatego polityka. Aby to zrobić, musi jednak wrócić do rodzinnego miasteczka i rozwieść się z pierwszym mężem.  ', \
                       '2013-01-02 02:10:00', '2013-01-02 03:50:00',\
                       '', actual)
        
        self.assertEqual(event.get_title(), "Dziewczyna z Alabamy")



if __name__ == '__main__':
    unittest.main()

