Instalację można przeprowadzić na kilka sposobów.

# Instalacja wersji stabilnej z PyPI #

[PyPI](https://pypi.python.org/pypi) jest centralnym indeksem różnych programów i bibliotek napisanych w Pythonie. Jest tam też najnowsza stabilna wersja [epguide](https://pypi.python.org/pypi/epguide).

Instalacja z PyPI jest najprostsza - niezbędne zależności są instalowane automatycznie.

W linii komend należy wpisać:
```
easy_install epguide
```
Lub dla NAS Synology:
```
easy_install-2.7 epguide
```

# Instalacja z pliku egg #

W przypadku gdy instalacja z PyPI jest niemożliwa (bo np. chcemy zainstalować wersję testową) należy:

  1. pobrać plik egg z strony głównej np. poleceniem
```
wget http://epguide.googlecode.com/hg/dist/epguide-1.7.2-py2.7.egg
```
  1. zainstalować z lokalnego pliku egg:
```
easy_install epguide-1.7.2-py2.7.egg
```
> gdzie zamiast 1.7.2 jest odpowiedni numer wersji aplikacji epguide

Przy użyciu tej metody easy\_install automatycznie ściągnie i zainstaluje potrzebne zależności.

# Użycie paczki ze źródłami #

Jeżeli są problemy z easy\_installa lub chcemy uruchomić program ze źródeł należy:

  1. pobrać plik ze źródłami np. poleceniem
```
wget http://epguide.googlecode.com/hg/dist/epguide-1.7.2.tar.gz
```
  1. rozpakować archiwum:
```
tar xfz epguide-1.7.2.tar.gz
```
> > Lub dla NAS Synology:
```
gunzip epguide-1.7.2.tar.gz
tar xf epguide-1.7.2.tar
```
  1. Może być potrzebne ręczne zainstalowanie zależności:

> Ubuntu:
```
sudo apt-get install libxml2
```
> oraz:
```
sudo easy_install libhttp2
sudo easy_install ConfigObj
```
  1. Uruchamianie poprzez:
```
epg_runner.py
```
> lub poprzez przykładowy plik skryptowy
```
run.sh
```
> dostępny na stronie [Skrypt](Skrypt.md)