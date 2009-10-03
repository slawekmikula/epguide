#!/bin/sh
#
# pobranie listy kanalow i odpowiadajacym im numerom mozna
# poprzez opcje -l
#
epguide -l

# backend Wirtualna Polska, kanaly zgodne z lista, dla calego tygodnia (od dzisiaj)
# format xmltv, wyjscie do pliku tv.xmltv
#
epguide -p wp -c 1,2,5,17,18,233 -w -f xmltv -o tv.xmltv

#
# backend Wp (domyslny), kanaly zgodne z lista, dla jednego dnia, format xmltv,
# wyjscie do pliku tv.xmltv
#
epguide -c 1,2,3 -d 2009-12-24 -f xmltv -o tv.xmltv
