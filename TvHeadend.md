Na końcu strony jest opis dla wersji 1.7.2.

# Opis dla wersji 1.8 #
## Zasada działania ##
  * w ramach instalacji epguide instaluje się skrypt `tv_grab_pl_epguide`, który ustawia się w Tvheadend dzięki czemu tvhedend uruchamia go cyklicznie i w ten sposób pobiera xmltv

## Przydatne linki ##
[TvHeadend](https://www.lonelycoder.com/redmine/projects/tvheadend/wiki/XML-TV_configuration)

## Szczegóły ##
  * Zainstalować epguide - patrz: [Instalacja](Instalacja.md)
  * Zalogować się **na konto użytkownika na którym uruchamiany jest tvheadend** (zazwyczaj użytkownik `hts`, czasami (np. na NAS Synology) - `tvheadend`) - uwaga nie używać ` su - ` bo są wtedy inne zmienne środowiskowe niż przy normalnym logowaniu.
  * sprawdzić czy uruchamia się `tv_grab_pl_epguide` (bez podawania ścieżki ani żadnych parametrów:
```
tv_grab_pl_epguide
```
  * jeżeli pojawi się komunikat, że nie jest skonfigurowany - należy go skonfigurować  - w tym celu:

### Konfiguracja tv\_grab\_pl\_epguide ###
  * uzyskać listę kanałów poprzez:
```
epguide -l
```

  * pojawi się lista kanałów (symbol - nazwa) z teleman.pl:
```
13-Ulica - 13 Ulica
4fun-TV - 4fun TV
ATM-Rozrywka - ATM Rozrywka
AXN - AXN
AXN-Black - AXN Black
AXN-Spin - AXN Spin
AXN-White - AXN White
Ale-Kino - ale kino+
Animal-Planet - Animal Planet
...
```
  * w jakimś edytorze tekstowym należy wpisać **symbole** kanałów dla których ma być pobierany program. Symbole należy oddzielać **przecinkami**. Na początkowym etapie testów lepiej podać mniej kanałów (np. dwa: `TVP-1,TVN`) a jak wszystko będzie działać to skonfigurować jeszcze raz podając więcej.

  * teraz należy skonfigurować `tv_grab_pl_epguide`, czyli uruchomić z opcją `--configure`:
```
tv_grab_pl_epguide --configure
```

  * na pytanie o kanały - wklejamy uprzednio przygotowaną listę kanałów
  * konfiguracja jest zapisana w pliku `~/.epguide/tv_grab_pl_epguide.ini` (można też zmieniać listę kanałów edytując ten plik)
  * ponownie uruchamiamy `tv_grab_pl_epguide` bez parametrów:
```
tv_grab_pl_epguide
```
  * po chwili (dłuższej lub krótszej w zależności od liczby pobieranych kanałów) na ekranie powinien pojawić się xml z programem czyli xmltv - teraz można przystąpić do konfiguracji Tvheadend

### Konfiguracja Tvheadend ###

  * w TvHeadend WebUI otworzyć panel `System Log` (mały przycisk ze "strzałkami" w prawym dolnym rogu). Alternatywnie można zrobić na konsoli `tail -f /var/log/syslog` (należy podać ścieżkę do logów sysloga)
  * w TvHeadend WebUI wybrać `Configuration`, `Channel / EPG`, `EPG Grabber`, w sekcji `Internal grabber`, podać:
    * `Module`: `XMLTV: Poland (epguide from teleman.pl)`
    * `Grab Interval` np. `8` `Hour`
    * nacisnąć `Save Configuration`
  * po każdym przestawieniu `Grab Interval` będzie wykonywany wybrany moduł czyli `tv_grab_pl_epguide` co powinno być widoczne w panelu System Log (lub w syslog) - u mnie wygląda to np. tak:
```
Jan 04 10:16:50 /usr/bin/tv_grab_pl_epguide: grab /usr/bin/tv_grab_pl_epguide
Jan 04 10:16:50 /usr/bin/tv_grab_pl_epguide: grab took 10 seconds
Jan 04 10:16:50 /usr/bin/tv_grab_pl_epguide: parse took 0 seconds
Jan 04 10:16:50 /usr/bin/tv_grab_pl_epguide:   channels   tot=    1 new=    0 mod=    0
Jan 04 10:16:50 /usr/bin/tv_grab_pl_epguide:   brands     tot=    0 new=    0 mod=    0
Jan 04 10:16:50 /usr/bin/tv_grab_pl_epguide:   seasons    tot=    0 new=    0 mod=    0
Jan 04 10:16:50 /usr/bin/tv_grab_pl_epguide:   episodes   tot=   26 new=   26 mod=   26
Jan 04 10:16:50 /usr/bin/tv_grab_pl_epguide:   broadcasts tot=   26 new=   26 mod=   26
```

> Jak widać są nowe audycje (broadcasts) dla 1 kanału.

  * teraz należy przejść na zakładkę `Channels` i dla każdego programu, który ma korzystać z xmltv w kolumnie `EPG Grap Source` wybrać odpowiedni wpis xmltv nazwa kanału
  * nacisnąć `Save changes`
  * teraz można przejśc na zakładkę `Electronic program guide` i odświeżyć (przycisk w lewym dolnym rogu) - powinny pojawić się audycje wczytane z xmltv



---


# Opis dla wersji 1.7.2 #
Uwaga: użyta tutaj metoda jest bardziej skomplikowana i dla nowszych wersji epguide (1.8 i nowsze) lepiej stosować opis powyżej.

## Zasada działania ##
  * epguide uruchamiany cyklicznie zapisuje do pliku `~/.xmltv/tv_grab_file.xmltv`
  * TvHeadend pobiera cyklicznie xmltv korzystając z `tv-grab-file`, który czyta z `~/.xmltv/tv_grab_file.xmltv`

## Przydatne linki ##
[TvHeadend](https://www.lonelycoder.com/redmine/projects/tvheadend/wiki/XML-TV_configuration)
[tv-grab-file](http://code.google.com/p/tv-grab-file/)

## Szczegóły ##
  * Zainstalować epguide
  * Zainstalować `tv_grab_file` z http://tv-grab-file.googlecode.com/files/tv_grab_file i skopiować do /usr/bin/
np.
```
wget http://tv-grab-file.googlecode.com/files/tv_grab_file
sudo cp tv_grab_file /usr/bin/tv_grab_file
```
  * sprawdzić kody interesujących nas kanałów przy pomocy `epguide -l`
  * utworzyć skrypt o nazwie np. `fetch_xmltv` pobierający epg - mój wygląda tak:
```
#!/bin/sh
epguide -t -c TVP-1,TVP-2 -f xmltv -o ~/.xmltv/tv_grab_file.xmltv
```
  * na koncie użytkownika TvHeadend (zazwyczaj `hts`) uruchomić skrypt `fetch_xmltv` - powinien powstać plik `~/.xmltv/tv_grab_file.xmltv`
  * w TvHeadend WebUI otworzyć panel System Log (mały przycisk ze "strzałkami" w prawym dolnym rogu). Alternatywnie można zrobić na konsoli `tail -f /var/log/syslog`
  * w TvHeadend WebUI wybrać Configuration, EPG Grabber, Internal grabber, XMLTV: tv\_grab\_file i podać Grab Interval np. 1 Hour oraz nacisnąć Save Configuration - po każdym przestawieniu Grab Interval będzie wczytywany plik xmltv co powinno być widoczne w panelu System Log (lub w syslog) - u mnie wygląda to np. tak:
```
Jan 04 10:16:50 /usr/bin/tv_grab_file: grab /usr/bin/tv_grab_file
Jan 04 10:16:50 /usr/bin/tv_grab_file: grab took 0 seconds
Jan 04 10:16:50 /usr/bin/tv_grab_file: parse took 0 seconds
Jan 04 10:16:50 /usr/bin/tv_grab_file:   channels   tot=    1 new=    0 mod=    0
Jan 04 10:16:50 /usr/bin/tv_grab_file:   brands     tot=    0 new=    0 mod=    0
Jan 04 10:16:50 /usr/bin/tv_grab_file:   seasons    tot=    0 new=    0 mod=    0
Jan 04 10:16:50 /usr/bin/tv_grab_file:   episodes   tot=   26 new=   26 mod=   26
Jan 04 10:16:50 /usr/bin/tv_grab_file:   broadcasts tot=   26 new=   26 mod=   26
```
Jak widać są nowe audycje (broadcasts) dla 1 kanału.
  * jeżeli plik wczytuje się poprawnie, to pozostaje dodanie do crona użytkownika `hts` cyklicznego uruchamiania skryptu `fetch_xmltv`