# -*- coding: utf-8 -*-
from epguide.parsers.teleman import TelemanProgrammeDetailsParser
import unittest
from epguide.data_formats import EventDetails
import codecs

class  TelemanProgrammeDetailsParserTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        pass

    def tearDown(self):
        pass

    def testGetDetails(self):
        p = TelemanProgrammeDetailsParser.TelemanProgrammeDetailsParser("a")
        f = codecs.open("Wrogowie-Publiczni-699775.html", "r", "UTF-8")
        buf = f.read()
        details = p.get_details(buf)
        f.close()
        description = u"USA, rok 1933. Po dziewięciu latach pozbawienia wolności John Dillinger (Johnny Depp) zostaje zwolniony warunkowo. \
Dokonuje on brawurowej akcji oswobodzenia kilku więźniów ze stanowego zakładu karnego w Michigan City. Pomaga mu John \"Red\" Hamilton (Jason Clarke). \
Po krótkim pobycie na odległej farmie dwaj wspólnicy oraz zbiegowie - Harry \"Pete\" Pierpont (David Wenham), Homer Van Meter \
(Stephen Dorff) i Ed Shouse (Michael Vieau) - przenoszą się do Chicago. Tam Dillinger i jego kompani dokonują serii śmiałych napadów na banki. \
Członkowie bandy zdobywają wielką popularność wśród zwykłych Amerykanów, zmęczonych wielkim kryzysem. \
Sam Dillinger związuje się ze śliczną Billie Frechette (Marion Cotillard). \
Przestępcy są nieuchwytni, a policja bezsilna. Dyrektor Biura Śledczego, J. Edgar Hoover (Billy Crudup), ogłasza Johna wrogiem publicznym numer jeden. \
Kierownictwo powierza zadanie złapania bandyty agentowi Melvinowi Purvisowi (Christian Bale), który stał się gwiazdą formującego się FBI po tym, \
jak zabił groźnego gangstera Pretty Boya Floyda (Channing Tatum). Rozpoczyna się pościg... \
Adaptacja książki Bryana Burrougha opowiada o ostatnim okresie życia legendarnego złoczyńcy."
        original_title = u"(Public Enemies)"
        year = u"2009"
        country = u"USA"
        genre = u"FILM GANGSTERSKI"
        imdb_url = u"http://www.imdb.com/Title?Public+Enemies+%282009%29"
        imdb_rank = u"7.0/10"
        filmweb_url = u"http://www.filmweb.pl/film/Wrogowie+publiczni-2009-467091"
        filmweb_rank = u"7.2/10"
        photo_url = u"http://media.teleman.pl/photos/470x265/Wrogowie-Publiczni.jpeg"
        pg = u"od 16 lat"
        expected = EventDetails(description, original_title, year, country, genre, imdb_url, imdb_rank, filmweb_url, filmweb_rank, photo_url, pg)
        print("description  :"+str(description))
        print("description  :"+description.encode('utf-8'))
        print("description  :"+str(details.description))
        print("description  :"+details.description.encode('utf-8'))
        print("actual  :"+str(details))
        print("expected:"+str(expected))
        self.assertEqual(details.description, expected.description)
        self.assertEqual(details.original_title, expected.original_title)
        self.assertEqual(str(details), str(expected))



if __name__ == '__main__':
    unittest.main()

