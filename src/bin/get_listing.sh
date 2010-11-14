#!/bin/sh
#
# pobranie listy kanalow i odpowiadajacym im numerom mozna
# poprzez opcje -l
#
epguide -l

# backend Canal+, kanaly zgodne z lista, dla calego tygodnia (od dzisiaj)
# format xmltv, wyjscie do pliku tv.xmltv
#
epguide -p cp -c ACA,ACZ -w -f xmltv -o tv.xmltv


# backend WpNg (domyslny), kanaly zgodne z lista, dla jednego dnia, format xmltv,
# wyjscie do pliku tv.xmltv
#
epguide -c 1,2,3 -d 2009-12-24 -f xmltv -o tv.xmltv
