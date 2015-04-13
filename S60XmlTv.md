# Wstęp #

Dokument opisuje sposób konfiguracji programu epguide do wygenerowania pliku wynikowego zgodnego z aplikacją TvGuide-S60 dla telefonów z systemem operacyjnym Symbian OS (Nokia, Samsung itp).

# Szczegóły #

Aby wygenerować plik i wczytać go do aplikacji należy:

  * Wybrać programy do sciągnięcia z listy:
```
$ epguide -l
```
  * Po wybraniu kanałów należy wywołać epguide z opcją sciągnięcia programu telewizyjnego w formacie xmltv z np. całego tygodnia i zapisanie go w skompresowanym formacie zip:
```
$ epguide -c 1,2 -w -f xmltv -o tv.xml
$ zip tv.xml.zip tv.xml
```
  * Przesłać plik tv.xml.zip do telefonu - do dowolnego katalogu
  * Uruchomić program TvGuide-S60 oraz 'Opcje'->'Dane'->'Wybierz plik danych' wybrać wgrany plik
  * Wywołać 'Dane'->'Odśwież'
  * Gotowe !