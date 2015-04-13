## Wstęp ##

Aplikacja pobiera dane z dowolnego źródła programu telewizyjnego. Obecnie obsługuje pobieranie z stron www.teleman.pl, tv.gazeta.pl. Wyjściem jest prosty format tekstowy lub format XMLTV.

## Do pobrania ##
  * 1.9.3 (EGG) - http://epguide.googlecode.com/hg/dist/epguide-1.9.3-py2.7.egg
  * 1.9.3 (TGZ) - http://epguide.googlecode.com/hg/dist/epguide-1.9.3.tar.gz

## Wiadomości ##
  * **2015/03/09** Wydanie wersji 1.9.3 Poprawka listowania kanałów teleman, poprawki kodowania utf8 dla formatu txt. Dzięki Łukasz !
  * **2014/12/06** Wydanie wersji 1.9.2 Poprawka w parsowaniu opcji --quiet w tv\_grab\_pl\_epguide
  * **2014/10/18** wydanie wersji 1.9.1 Zawiera możliwość określenia listy kanałów z wersji 1.9.0 dla interfejsu tv\_grab\_pl

  * **2014/10/15** wydanie wersji 1.9.0. Dodano możliwość określenia list kanałów z parserami dla każdego z osobna. Więcej w readme. (#6)

  * **2014/03/09** wydanie wersji 1.8.1. Poprawiono parsowanie strony teleman. Zmiana lokalizacji plików do pobrania.

  * **2013/11/20** wydanie wersji 1.8.0: Poprawa parsowania programu po zmianach na teleman.pl (#30), Dodanie obrazka dla programu (#31)

  * **2013/08/18** wydanie wersji 1.7.2: url dla obrazka kanału (#23), wiek dopuszczalny w tytule programu (#24), tytuł oryginalny + rok produkcji (#26), liczba pobieranych dni --days (#27), poprawki błędów i zmian w parserach

  * **2013/04/12** wydanie wersji 1.7.1: dodanie ściągania szczegółów opisów (damian #19), poprawienie parsowania kanałów bez opisu tekstowego (#21), poprawienie wyjścia na konsolę (#20)

  * **2012/10/31** wydanie wersji 1.7.0: usunięcie parsera wp.pl (całkowita zmiana layoutu strony), domyślny parser to teleman, wprowadzenie poprawek parsowania teleman (thx jacek), poprawka parsowania daty (#15)

  * **2012/05/31** - wydanie wersji 1.6.0 - porządki w kodzie - usunięcie starego parsera strony wp.pl, usunięcie nie działającego parsera canal+, parser teleman poprawiony do najnowszej wersji strony teleman.pl

  * **2010/11/14** - wydanie wersji 1.5.0 - dodanie parsera canal+ (dzięki Michał Sawicz), możliwość podawania identyfikatorów kanałów w postaci tekstowej (dla canal+)

  * **2010/06/22** - wydanie wersji 1.4.3 - poprawki #8, #10 - poprawka formatowania strefy czasowej, dodanie logowania operacji - nowa opcja linii komend '--verbose'

  * **2010/04/16** - wydanie wersji 1.4.2 - poprawki #8, #9 - teleman i nazwy kanałów, xml formatowanie strefy czasowej

  * **2010/04/01** - wydanie wersji 1.4.1 - poprawka #7 - parsowanie wszystkich kategorii dla teleman

  * **2010/03/30** - wydanie wersji 1.4 - zmiana domyślnego parsera na wpng, serwis tv.wp.pl zmienił layout na nowy. Korzystamy tylko z parsera wpng

  * **2010/03/24** - wydanie wersji 1.3 - dodanie parserów beta.tv.wp.pl oraz teleman, możliwość zapisu kategorii programu (teleman), zamknięcie #3, #5

  * **2009/12/19** - wydanie wersji 1.2 - poprawa zgłoszonego błędu #1, #4

  * **2009/12/19** - wydanie wersji 1.1 - skrypt startujacy bezposrednio z archiwum epguide\_run

  * **2009/10/04** - prace nad stronami Wiki. Nowe strony opisujące możliwości i programy wykorzystujące format XMLTV

  * **2009/10/03** - zmiana repozytorium kodu na mercurial, wgranie wersji 1.0 aplikacji. Zmiana wewnętrznej struktury aplikacji tak aby istniała możliwość rozszerzania o inne formaty we/wy

  * **2008/03/21** - przeniesienie źródeł z zewnętrznego repozytorium u Michała (dzięki za całą aktualną pomoc!). Zdecydowałem, że dla ewentualnego dalszego rozwoju kodu, umieszczę go na serwerze do którego każdy, nie tylko ja, będzie miał dostęp w dowolnym czasie. Co do samej aplikacji rozpocząłem prace nad przebudową kodu.


## Archiwum ##
  * (EGG) - http://epguide.googlecode.com/hg/dist/
  * (TGZ) - http://epguide.googlecode.com/hg/dist/

## Wiki ##

Na wiki umieszczone zostały ogólne informacje o korzystaniu z aplikacji, możliwościach dalszego rozwoju oraz współpracy nad kodem.