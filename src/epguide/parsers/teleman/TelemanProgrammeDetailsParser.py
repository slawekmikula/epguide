# -*- coding: utf- 8 -*-
from epguide.data_formats import Imdb, ParentalRating
from lxml import etree
import StringIO
import re
from epguide.parsers.teleman.TelemanData import TelemanEventDetails
from epguide.parsers.AbstractParser import AbstractParser
 
class TelemanProgrammeDetailsParser(AbstractParser):
                    
    def get_details(self, buf):
        """
        parsuje stronę, zwraca liste elementow
        klasy Event
        """

        parser = etree.HTMLParser()
        tree = etree.parse(StringIO.StringIO(buf), parser)
        primary_title = self.get_texts(tree, "id('showOverview')/div/h1[@class='title primary-title']/a")
        if len(primary_title.strip()) == 0:
            primary_title = self.get_texts(tree, "id('showOverview')/div/h1[@class='title']")
        secondary_title = self.get_texts(tree, "id('showOverview')/div/h2[@class='title']")        
# Opis 
#----
# /html/body/div/div[5]/div[3]/h2
# html body.show div#wrapper.container div#content div.section h2
#
#
# <div class="section">
#  <h2>Opis</h2>
#  <p>Zły Maltazar przedostaje się do świata ludzi, gdzie uzyskuje wzrost ponad dwóch metrów. Razem z armią gigantycznych moskitów postanawia opanować Ziemię. Powstrzymać go może tylko Artur, który jednak uwięziony jest w milimetrowym ciele. Chłopiec próbuje powrócić do swojej dawnej postaci. Pomagają mu w tym przyjaciele z krainy Minimków, księżniczka Selenia i Betamesz. Razem wyruszają po magiczny miód Królowej Pszczół, który pozwoli odzyskać Arturowi dawny wzrost. Nieoczekiwanie podróżnicy otrzymują pomoc ze strony Darkosa, demonicznego syna Maltazara. Trzecia część cyklu o malutkich stworkach żyjących w ogródku babci. Za całą trylogię odpowiada francuski reżyser <a href="/osoby/Luc-Besson-12379">Luc Besson</a>.</p>
# </div>
#
        in_this_episode = self.get_texts(tree, "id('content')/div[@class='section' and contains(h2/text(), 'W tym odcinku')]/p")
        if in_this_episode:
            description = "\nW tym odcinku: "+in_this_episode
        else:
            description = ""
        description += "\nOpis: "+self.get_texts(tree, "id('content')/div[@class='section' and contains(h2/text(), 'Opis')]/p") 
#        print("description:" + description)
#
# Tytuł oryginalny
#----------------
# /html/body/div/div[5]/div/h2
# html body.show div#wrapper.container div#content div#showOverview h2.orig-title
#
# <h2 class="orig-title">(Arthur et la guerre des deux mondes)</h2>
#
        original_title = self.get_texts(tree, "id('showOverview')/h2[@class='orig-title']")  # //h2[@class='orig-title']
        if original_title.startswith('(') and original_title.endswith(')'):
            original_title = original_title[1:-1]
        if len(original_title.strip()) == 0:
            original_title = None

#        print("original title:" + original_title)
# Rok
#---
# /html/body/div/div[5]/div/div[2]/ul/li[3]
# html body.show div#wrapper.container div#content div#showOverview div#showMainInfo ul li
#
# <li>2010</li>
        year = self.get_texts(tree, "//div[@id='showMainInfo']/span[5]")
#        print("year:" + year)
#
# Kraj
#----
# /html/body/div/div[5]/div/div[2]/ul/li[2]
# html body.show div#wrapper.container div#content div#showOverview div#showMainInfo ul li
#
# <li>Francja</li>
        country = self.get_texts(tree, "//div[@id='showMainInfo']/span[3]")
#        print("country:" + country)
#
# Rodzaj
#------
# /html/body/div/div[5]/div/div[2]/ul/li
# html body.show div#wrapper.container div#content div#showOverview div#showMainInfo ul li
#
# <li>FILM PRZYGODOWY</li>
        genre = self.get_texts(tree, "//div[@id='showMainInfo']/span[1]")
#        print("genre:" + genre)
#
# IMDB
#----
# /html/body/div/div[5]/div/a
# html body.show div#wrapper.container div#content div#showOverview a.imdb-rank

# <a target="_blank" rel="nofollow" title="zobacz stronę tego filmu w bazie IMDb (ang.)" href="http://www.imdb.com/Title?Public+Enemies+%282009%29" class="imdb-rank"><strong>7.0</strong>/10</a>
        imdb_url = self.get_attr(tree, "//div[@id='showOverview']/a[contains(@class,'imdbRank')]", "href")
        imdb_rank = self.get_texts(tree, "//div[@id='showOverview']/a[contains(@class,'imdbRank')]/strong")
        imdb = Imdb(imdb_url, imdb_rank)
#        print("imdb:" + str(imdb))
#
# Filweb
#------
# /html/body/div/div[5]/div/a[2]
# html body.show div#wrapper.container div#content div#showOverview a.fw-rank
#
# <a onclick="_gaq.push(['_trackEvent','Outbound Links','Click',this.href]);setTimeout(window.open(this.href));return false" target="_blank" rel="nofollow" title="zobacz stronę tego filmu w serwisie Filmweb.pl" href="http://www.filmweb.pl/film/Toy+Story+3-2010-172884" class="fw-rank"><div class="label">Filmweb</div><div class="value"><strong>7.3</strong>/10</div></a>  
#
        filmweb = self.get_texts(tree, "//div[@id='showOverview']/a[contains(@class,'filmwebRank')]")
        filmweb_url = self.get_attr(tree, "//div[@id='showOverview']/a[contains(@class,'filmwebRank')]", "href")
        filmweb_rank = self.get_texts(tree, "//div[@id='showOverview']/a[contains(@class,'filmwebRank')]/strong")
        filmweb = Imdb(filmweb_url, filmweb_rank)
#        print("filmweb:" + str(filmweb))
# Photo
#-----
# /html/body/div/div[5]/div/div/img
# html body.show div#wrapper.container div#content div#showOverview div.photo img
#
# <img width="470" height="264" alt="Artur i Minimki 3. Dwa światy" src="http://media.teleman.pl/tmdb/470x265/hJ7zcIAxY3cfavFmsfz2JetRQ1x.jpg">
# <a target="_blank" rel="nofollow" title="zobacz stronę tego filmu w bazie IMDb (ang.)" href="http://www.imdb.com/Title?Arthur+et+la+guerre+des+deux+mondes+%282010%29" class="imdb-rank"><strong>5.3</strong>/10</a>
#
        photo_url = self.get_attr(tree, "//div[@id='showOverview']/div[@id='showPhoto']/img", "src")
#        print("photo_url:" + photo_url)
#
# PG
# --
# /html/body/div/div[5]/div/div[2]/span
# html body.show div#wrapper.container div#content div#showOverview div#showMainInfo span.age-rating
#
# <span title="kategoria wiekowa &mdash; bez ograniczeń" class="age-rating age-rating-bo">b.o.</span>
# <span title="kategoria wiekowa &mdash; od 7 lat" class="age-rating age-rating-po7">od 7 lat</span>
# <span title="kategoria wiekowa &mdash; od 12 lat" class="age-rating age-rating-po12">od 12 lat</span>
#
        pg_desc = self.get_texts(tree, "//div[@id='showMainInfo']/span[contains(@class,'age-rating')]")
        if pg_desc == "b.o.":
            min_age = 0
        else:
            ageregexp = re.compile('od (\d*) lat',re.DOTALL)
            m = ageregexp.search(pg_desc)
            if m is None: 
                min_age = 0
            else:
                if m.group(1) is None:
                    min_age = 0
                else:
                    min_age = int(m.group(1))

        pg = ParentalRating(pg_desc, min_age)
        #print("pg:" + str(pg))
# Występują, reżyser,opis
#-------------------------
# //*[@id="show-more-info"]
# html body.show div#wrapper.container div#content div#showOverview table#show-more-info
#
#
# <table cellspacing="0" id="show-more-info">
#    <tbody><tr><th>Występują:</th><td><a href="/osoby/Freddie-Highmore-12380">Freddie Highmore</a>, <a href="/osoby/Mia-Farrow-11095">Mia Farrow</a>, <a href="/osoby/Penny-Balfour-12382">Penny Balfour</a>, <a href="/osoby/Robert-Stanton-13876">Robert Stanton</a></td></tr>
#    <tr><th>Reżyseria:</th><td><a href="/osoby/Luc-Besson-12379">Luc Besson</a></td></tr>
#    <tr><th>W skrócie:</th><td>Maltazar przedostaje się do świata ludzi w celu przejęcia władzy nad Ziemią przy pomocy gigantycznych moskitów. Do akcji wkracza Artur.</td></tr>
#  </tbody></table>
#  
        cast = self.get_texts(tree, "//div[@id='showOverview']/table[@id='show-more-info']/tbody/tr[1]/td")
        #print("cast:" + cast)
        director = self.get_texts(tree, "//table[@id='show-more-info']/tbody/tr[2]/td/a")
        #print("director:" + director)
#  
# Nagrody
#-------
# //*[@id="section-awards"]
# html body.show div#wrapper.container div#content div#section-awards.section
#
# <div id="section-awards" class="section">
#  <h2>Nagrody</h2>
#  <p>Oscar, Złoty Glob</p>
# </div>
#        awards = self.get_texts(tree, "//div[@id='showMainInfo']/span")
#        print("awards:"+awards)
        
        return TelemanEventDetails(primary_title, secondary_title, description, original_title, year, country, genre, imdb, filmweb, photo_url, pg)
    
