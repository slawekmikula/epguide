#!/usr/bin/python
#
# License: GPL
#
# This module parses a TV program guide from wp.pl (a Polish portal)
#
# xmltv parser got form internet (could not find today the name of the blog/author)
# added xmltv output, parsing weeks, days etc.
#
# modified by Slawek Mikula <zorba@silesianet.pl>

import time
import common
import wpparser
import sys, getopt, datetime, urllib

monthTable = [31,28,31,30,31,30,31,31,30,31,30,31]

if __name__ == "__main__":
  
  err = sys.stderr
 
  opts, args = common.parse_opts(sys.argv)

  url_template = "http://tv.wp.pl/index_druk.html?T[date]=%s&T[station]=%s&T[time]=0"
  date = time.strftime ("%Y-%m-%d", opts.date)
  
  # jesli lista kanalow
  if opts.list:
    
    for i in range(1,512):
      url = url_template % (date, i)
      buf = urllib.urlopen (url).read()

      p = wpparser.WPParser()
      p.feed(buf)
      p.close()

      if p.success:
        print "ID: %4d CHANNEL: %s" % (i, p.channel)
      else:
        pass

  elif opts.getWeek:    

    chans = []
    # print header
    print common.header(opts.format)  
    
    # for a whole week
    firstTime = True    
    for date_iter in range(0,7):
        
        # pobieramy miesiac
        year = time.strftime ("%Y", opts.date)
        year = int(year)        
        
        month = time.strftime ("%m", opts.date)
        month = int(month)
        dayInMonth = monthTable[month - 1]
        
        day = time.strftime ("%d", opts.date)
        day = int(day) + date_iter
        
        if day > dayInMonth :
            day = day - dayInMonth
            if month < 12:
                month = month + 1
            else :
                month = 1
                year = year + 1
            
        year = str(year)
        month = str(month)
        day = str(day)

        
        if len(day) == 1:
            day = "0" + day
        if len(month) == 1:
            month = "0" + month
        
        date_now = str(year) + "-" + str(month) + "-" + str(day)
        
        print >> err, date_now
        
        channelList = opts.channelList.split(',')

        for i in channelList:
            url = url_template % (date_now, i)
            buf = urllib.urlopen (url).read()

            p = wpparser.WPParser()
            p.feed(buf)
            p.close()

            if p.success:
                chans.append(common.Channel(p.chanid,p.channel,p.programs,p.date))            
            else:
              print >> err, "error: failed to parse the page: %s" % url
              
        if firstTime:
            for chan in chans:
                print common.format_channel (chan, opts.format),
                firstTime = False
        for chan in chans:
            print common.format_output (chan, opts.format),
        
          
    # print footer  
    print common.footer(opts.format)      
    
  else:
    # print header
    chans = []
    print common.header(opts.format)  
    
    year = time.strftime ("%Y", opts.date)
    month = time.strftime ("%m", opts.date)
    day = time.strftime ("%d", opts.date)
        
    date_now = str(year) + "-" + str(month) + "-" + str(day)
        
    print >> err, date_now
        
    channelList = opts.channelList.split(',')
    for i in channelList:
        url = url_template % (date_now, i)
        buf = urllib.urlopen (url).read()

        p = wpparser.WPParser()
        p.feed(buf)
        p.close()
        
        if p.success:
            chans.append(common.Channel(p.chanid,p.channel,p.programs,p.date))            
        else:
          print >> err, "error: failed to parse the page: %s" % url

    for chan in chans:
        print common.format_channel (chan, opts.format),
    for chan in chans:
        print common.format_output (chan, opts.format),

    # print footer  
    print common.footer(opts.format)          
    
