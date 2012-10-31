#!/bin/sh
#
# pobranie listy kanalow i odpowiadajacym im numerom mozna
# poprzez opcje -l
#
epguide -l

# backend teleman, kanaly zgodne z lista, dla jednego dnia, format xmltv,
# wyjscie do pliku tv.xmltv
#
epguide -c 1,2,3 -d 2012-10-30 -f xmltv -o tv.xmltv
