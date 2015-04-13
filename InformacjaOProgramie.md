**EpGuide**

## O programie ##

Program jest prostym parserem stron przedstawiających polskie programy telewizyjne.
Obecnie bazuje na danych ze strony www.teleman.pl.
Program w wyniku swojej pracy dostarcza wyniku w postaci pliku tekstowego lub
pliku w formacie [xmltv](http://wiki.xmltv.org). Pozwala to na prostą integrację z aplikacjami
wykorzystującymi ten format pliku (XMLTV) do wyświetlania aktualnego programu
telewizyjnego

## Licencja ##
Program jest na licencji GNU. Pełna treść licencji znajduje się w pliku LICENSE.

## Instalacja ##
Różne sposoby instalacji są opisane na stronie [Instalacja](Instalacja.md)

## Użycie ##
Uruchomienie polega na wywolaniu epguide z odpowiednimi opcjami.

Wywolanie z opcją `--help` wyswietli wszystkie dostepne opcje

Poczatkowo nalezy uruchomić program z opcją `-l`, co wyświeli wszystkie
kanały telewizyjne obsługiwane przez dostarczyciela programu - ich identyfikatory i nazwy. Domyślnym i aktualnie jedynym dostarczycielem jest teleman.pl. Następnie wymagane identyfikatory kanałów należy umieścić w wywołaniu głównym programu. Program ma możliwość eksportowania listy programów do formatu txt lub XMLTV.

## Wylistowanie dostępnych kanałów ##
Uruchamiamy program z opcją `-l`. Domyślnie epguide wylistuje listę dostępnych
kanałów wraz z ich identyfikatorami na standardowe wyjście

```
$ epguide.py -l
```

## Sciągnięcie listy programów ##
Przykladowe uzycie do sciagniecia calotygodniowego programu telewizyjnego
dla stacji TVP1 TVP2  TVN Polsat TV4:

```
$ epguide.py -c TVP-1,TVP-2,TVN,Polsat,TV4 -f xmltv -w -o tv.xml
```

## Ściągnięcie listy programów od wielu dostawców ##
W przypadku, gdy chcemy ściągnąć pojedynczą listę kanałów (plik) od wielu
dostawców z różnymi kanałami możemy użyć specjalnej opcji definicji listy
kanałów. W przypadku podania listy kanałów jako lista określająca przez
[parser|kanał,]**aplikacja ściągnie poszczególne kanały z listy przez
podany parser. Przykład:**

```
$ epguide -c gazeta|1,teleman|POLSAT -f xmltv -w -o tv.xml
```