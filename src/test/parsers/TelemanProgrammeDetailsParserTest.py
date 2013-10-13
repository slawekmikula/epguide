# -*- coding: utf-8 -*-
from epguide.parsers.teleman import TelemanProgrammeDetailsParser
import unittest
from epguide.data_formats import Event, Imdb, ParentalRating, ParserOptions, Channel
import codecs
from epguide.parsers.teleman.TelemanData import TelemanEventDetails, TelemanEvent
from epguide.util import to_string

class  TelemanProgrammeDetailsParserTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        pass

    def tearDown(self):
        pass

    def testGetDetails(self):
        p = TelemanProgrammeDetailsParser.TelemanProgrammeDetailsParser("a")
        f = codecs.open("Wrogowie-Publiczni-699775.html", "r", "UTF-8")
        #http://www.teleman.pl/tv/Wrogowie-Publiczni-699775
        buf = f.read()
        actual = p.get_details(buf)
        f.close()
        expected_description = u"\nOpis: USA, rok 1933. Po dziewięciu latach pozbawienia wolności John Dillinger (Johnny Depp) zostaje zwolniony warunkowo. \
Dokonuje on brawurowej akcji oswobodzenia kilku więźniów ze stanowego zakładu karnego w Michigan City. Pomaga mu John \"Red\" Hamilton (Jason Clarke). \
Po krótkim pobycie na odległej farmie dwaj wspólnicy oraz zbiegowie - Harry \"Pete\" Pierpont (David Wenham), Homer Van Meter \
(Stephen Dorff) i Ed Shouse (Michael Vieau) - przenoszą się do Chicago. Tam Dillinger i jego kompani dokonują serii śmiałych napadów na banki. \
Członkowie bandy zdobywają wielką popularność wśród zwykłych Amerykanów, zmęczonych wielkim kryzysem. \
Sam Dillinger związuje się ze śliczną Billie Frechette (Marion Cotillard). \
Przestępcy są nieuchwytni, a policja bezsilna. Dyrektor Biura Śledczego, J. Edgar Hoover (Billy Crudup), ogłasza Johna wrogiem publicznym numer jeden. \
Kierownictwo powierza zadanie złapania bandyty agentowi Melvinowi Purvisowi (Christian Bale), który stał się gwiazdą formującego się FBI po tym, \
jak zabił groźnego gangstera Pretty Boya Floyda (Channing Tatum). Rozpoczyna się pościg... \
Adaptacja książki Bryana Burrougha opowiada o ostatnim okresie życia legendarnego złoczyńcy."
        expected_primary_title = u"Wrogowie publiczni"
        expected_secondary_title = ""
        expected_original_title = u"Public Enemies"
        expected_year = u"2009"
        expected_country = u"USA"
        expected_genre = u"FILM GANGSTERSKI"
        expected_imdb_url = u"http://www.imdb.com/Title?Public+Enemies+%282009%29"
        expected_imdb_rank = u"7.0/10"
        expected_imdb = Imdb(expected_imdb_url, expected_imdb_rank)
        expected_filmweb_url = u"http://www.filmweb.pl/film/Wrogowie+publiczni-2009-467091"
        expected_filmweb_rank = u"7.2/10"
        expected_filmweb = Imdb(expected_filmweb_url, expected_filmweb_rank)
        expected_photo_url = u"http://media.teleman.pl/photos/470x265/Wrogowie-Publiczni.jpeg"
        expected_pg = ParentalRating(u"od 16 lat", 16)
        expected = TelemanEventDetails(expected_primary_title, expected_secondary_title, expected_description, expected_original_title, expected_year, expected_country, expected_genre, expected_imdb, expected_filmweb, expected_photo_url, expected_pg)
        print("expected_description  :"+str(expected_description))
        print("expected_description  :"+expected_description.encode('utf-8'))
        print("expected_description  :"+str(actual.description))
        print("expected_description  :"+actual.description.encode('utf-8'))
        print("actual  :"+to_string(actual))
        print("expected:"+to_string(expected))
        self.assertEqual(actual.description, expected.description)
        self.assertEqual(actual.original_title, expected.original_title)

        self.assertEqual(to_string(actual.filmweb), to_string(expected.filmweb))
        self.assertEqual(to_string(actual.imdb), to_string(expected.imdb))
        self.assertEqual(to_string(actual.pg), to_string(expected.pg))
        self.assertEqual(actual.photo_url, expected.photo_url)
        
        self.assertEqual(str(actual), str(expected))
        parserOptions = ParserOptions()
        channel = Channel('TVP-1', 'TVP 1')
        event = TelemanEvent(parserOptions, channel, 'Liberator 2', \
                       'Movie/Drama', 'film sensacyjny, USA 1995', \
                       'Terrory\xc5\x9bci opanowuj\xc4\x85 luksusowy poci\xc4\x85g. ', \
                       '2013-01-02 02:10:00', '2013-01-02 03:50:00',\
                       '', actual)
        self.assertEqual(event.get_title(), "Liberator 2")



if __name__ == '__main__':
    unittest.main()

