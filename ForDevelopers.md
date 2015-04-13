# Wstęp #

Dokument przedstawia informacje o współtworzeniu aplikacji, sposobie budowania, wydawania nowych wersji oraz wszystkich tych informacjach, które przydają się jeśli chce ktoś pomóc w jej rozwoju.

# Współpraca #

Każdy jest zaproszony do współtworzenia aplikacji. Można pomagać na wiele sposobów:
  * **współtworzyć kod** - wystarczy utworzyć własny klon kodu źródłowego, pobrać do własnego repozytorium i można zacząć pracować nad nowymi funkcjonalnościami !
  * **zgłaszać nowe pomysły** - można zapisywać potrzeby nowych funkcjonalności i spostrzeżeń z działania aplikacji. Nie gwarantujemy odpowiedzi natychmiastowej, ale zapisanie takiego zgłoszenia w miejscu [Issues](http://code.google.com/p/epguide/issues/list) pozwoli na zajęcie się tym tematem w najbliższym możliwym czasie
  * **raportować błędy** - takie informacje są niezmiernie przydatne przy zapewnieniu jak najlepszej jakości aplikacji. Nie wszystko można samodzielnie przewidzieć poczas tworzenia nowej funkcjonalności. Zgłaszając błąd prosimy o jak najwięcej informacji, które pozwolą w szybki i pewny sposób znaleźć rozwiązanie. Wszystkie zgłoszenia błędów są przez nas traktowane bardzo poważnie. Jak poprawnie zgłosić błąd ? Patrz [tutaj](http://www.chiark.greenend.org.uk/~sgtatham/bugs-pl.html)

# Kod źródłowy #

Kod źródłowy dostępny jest bezpośrednio ze strony projektu: [Sources](http://code.google.com/p/epguide/source/checkout). Projekt korzysta z Mercuriala jako repozytorium przechowywania kodu źródłowego. Zarówno w systemie windows jak i linux istnieje multum nakładek i wtyczek do środowisk programistycznych pozwalających w prosty sposób pobrać kod źródłowy na własny dysk.
**UWAGA!** Repozytorium kodu może zawierać nowe funkcjonalności zgodnie z cyklem pracy projektantów. Zawsze staramy się, aby kod, który się tam znajduje był poprawny i działający. Jednak nie miejcie do nas pretensji, gdy nie do końca jest w idealnym stanie. W końcu to przecież repozytorium :)

# Wydania #

Każdorazowo, gdy decydujemy o tym, iż wprowadzona nowa funkcjonalność osiągnęła stan stabilny decydujemy o wydaniu nowej wersji programu. W takim przypadku pojawia się ona (informacja) na serwisie Python Package Index (pypi.python.org) oraz kod źródłowy w formie archiwum oraz pakiet egg pojawiają się na stronie pobierania: [Downloads](http://code.google.com/p/epguide/downloads/list)

# Środowisko programistyczne #

Do współtworzenia oprogramowania nie potrzebujemy żadnego specjalistycznego oprogramowania. Aktualnie twórcy programu korzystają z Eclipe PyDev lub Netbeans i takie definicje projektów znajdują się w repozytorium projektu.

# Praca z kodem #

W przypadku pracy nad kodem i proponowania nowych funkcjonalności można zaprezentować nam Wasz udział na kilka sposobów:
  * Utworzyć zgłoszenie nowej funkcjonalności i dołączyć plik łatki (patch)
  * Utworzyć zgłoszenie przeglądu kodu i dodać tam łatkę (patch)
  * Utworzyć własny klon repozytorium oraz prowadzić tam prace, następnie poprosić o połączenie kodu (push request)
  * Otrzymać dostęp do głównego repozytorium kodu jako współtwórca

# Release aplikacji #

Prace wstępne, które należy wykonać przed publikowaniem:
  * zmienić odpowiednie parametry wersji w plikach Makefile, setup.py
  * zaktualizować plik CHANGES/TODO o informacje wprowadzone od ostaniej wersji
  * sprawdzić, czy wszystkie nowe pliki (jeśli zostały dodane do projektu są w odpowiednich definicjach setup.py oraz EGG-INFO)

W celu zbudowania nowej wersji aplikacji i umieszczeniu ich w odpowiednich miejscach projektu należy:
  * posiadać załozone konto na Python Package Index (pypi.python.org)
  * otrzymać uprawnienia typu Maintainer (admini projektu) do wprowadzania nowej informacji na PyPi
  * **make egg** - zostanie utworzony w katalogu dist wynikowy plik EGG (np. epguide-1.7.1-py2.7.egg
  * **make dist** - zostanie utworzony w katalogu dist wynikowy plik tar.gz z archiwum projektu (np. epguide-1.7.2.tar.gz)
  * **make pypi** - zostanie opublikowana informacja na stronie Python Package Index o nowej wersji oprogramowania
  * **wgrać pliki wynikowe** do projektu google-code i oznaczyć je jako Featured (zostaną wtedy promowane na głównej stronie)
  * **starej wersji zmienić status** na "Deprecated" co ukryje je przed widocznością przy bezpośrednim wejściu do pobierań
  * opisać na stronie głównej (poprzez zakładkę administracji) informacje o nowej wersji
  * i ... gotowe :)