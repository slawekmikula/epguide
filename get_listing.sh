#!/bin/sh
# pobiera listing programow z calego tygodnia od dnia dzisiejszego
# z kanalow o numerach 1,2,5,17,18,233
# tj. TVP1, TVP2, POLSAT, TVN, TVP3 Regionalna, TV4
# 1,2,5,17,18,233
#
# pobranie listy kanalow i odpowiadajacym im numerom mozna
# poprzez opcje -l
#
# wiecej w epguide --help

# uzycie pliku konfiguracji, wyjscie do pliku tv.xmltv
#
#  epg_runner --config 'input.conf' --output tv.xmltv
#
# backend Canal+, kanaly zgodne z lista, dla calego tygodnia (od dzisiaj)
# format xmltv, wyjscie do pliku tv.xmltv
#
# epg_runner -b cp -c '1,2,5,17,18,233' -w -f xmltv -o tv.xmltv
#
# backend Wp (domyslny), kanaly zgodne z lista, dla jednego dnia, format xmltv,
# wyjscie do pliku tv.xmltv
#
# epg_runner -c '1,2,3' -d '2007-08-12' -f xmltv -o tv.xmltv