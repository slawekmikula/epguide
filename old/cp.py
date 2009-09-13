#!/usr/bin/python
import common
import urllib
import cpparser
import re
import sys
import time
import datetime

if __name__ == "__main__":  
    err = sys.stderr
    opts, args = common.parse_opts(sys.argv)
    date = time.strftime ("%Y-%m-%d", opts.date)
       
    # jesli lista kanalow
    if opts.list:
        sock = urllib.urlopen("http://www.cyfraplus.pl/cgi-bin/cyf/index")
        cplist = cpparser.CPList()
        cplist.feed(sock.read())
        for chan in cplist.chans:
            print chan['id'], ":", chan['name'].encode("utf-8"), "(xmltv: "+re.sub("[^a-z0-9]", "", chan['name'].strip().lower())+".cplus)".encode("utf-8")
          
    elif opts.getWeek:
        print common.header(opts.format)
        printChannels = True
        
        chans = "&can="+"&can=".join(opts.channelList.split(','))

        for i in range(7):
            data = (datetime.date.today() + datetime.timedelta(days=i))
            print >> err,data
            attrs = urllib.urlencode({'action': 'day-find', 'dmin': data.strftime("%Y.%m.%d"), 'dmax': data, 'full': 1, 'toprint' : '_print'})
            sock = urllib.urlopen("http://www.cyfraplus.pl/cgi-bin/cyf/index", attrs+chans)
            
            p = cpparser.CPParser()
            p.rok = data.strftime("%Y")
            p.feed(sock.read())
            p.close()
            
            if p.success:
                if printChannels:
                    for chan in p.chans:
                        print common.format_channel (chan, opts.format),
                        printChannels = False
                for chan in p.chans:
                    print common.format_output (chan, opts.format),
            
        print common.footer(opts.format)
      
    else:
        print common.header(opts.format)  
        
        data = time.strftime("%Y.%m.%d", opts.date)

        print >> err, data
        
        chans = "&can="+"&can=".join(opts.channelList.split(','))
        attrs = urllib.urlencode({'action': 'day-find', 'dmin': data, 'dmax': data, 'full': 1, 'toprint' : '_print'})
        sock = urllib.urlopen("http://www.cyfraplus.pl/cgi-bin/cyf/index", attrs+chans)

        p = cpparser.CPParser()
        p.rok = time.strftime("%Y", opts.date)
        p.feed(sock.read())
        p.close()
        
        if p.success:
            for chan in p.chans:
                print common.format_channel (chan, opts.format),
            for chan in p.chans:
                print common.format_output (chan, opts.format),
        else:
            print >> err, "error: failed to parse the page"
        
        print common.footer(opts.format)
        
                