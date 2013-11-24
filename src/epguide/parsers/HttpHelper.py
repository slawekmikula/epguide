# -*- coding: utf-8 -*-
'''
Created on 25-02-2013

@author: Damian
'''

from httplib2 import Http, FileCache
import httplib2
import os
import logging
import datetime
import shutil

class HttpHelper(object):
    '''
    classdocs
    '''

    def __init__(self, enable_debug):
        self.log = logging.getLogger(__name__)
        today = datetime.date.today()
        previousMonth =  today - datetime.timedelta(days=31)
        prevoiusMonthSubDir = previousMonth.strftime("%Y-%m")
        
        cache_dir_to_remove = os.path.join(os.path.normpath(os.path.expanduser("~/.epguide/cache")), prevoiusMonthSubDir)
        if os.path.exists(cache_dir_to_remove):
            self.log.info("Removing previous month cache dir: " + cache_dir_to_remove)
            try:
                shutil.rmtree(cache_dir_to_remove)
                self.log.info("Removed.")
            except Exception:
                self.log.exception("Exception while removing dir " + cache_dir_to_remove)
        else:
            self.log.info("Previous month cache dir not exists: " + cache_dir_to_remove)
            
        thisMonthSubDir = today.strftime("%Y-%m")
        cache_dir = os.path.join(os.path.normpath(os.path.expanduser("~/.epguide/cache")), thisMonthSubDir)
        self.log.info("Cache dir: " + cache_dir)
        self.cache = FileCache(cache_dir)
        self.http = Http(cache = self.cache)
        self.user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0"
        if(enable_debug):
            httplib2.debuglevel = 255
        
    def get(self, url, force_cache = False, charset = "UTF-8"):
        if(force_cache):
            cached_value = self.cache.get(url)
            if cached_value:
                try:
                    info, content = cached_value.split('\r\n\r\n', 1)
                    if(content):
                        return content.decode(charset)
                    else:
                        return self.get(url, False, charset)
                except (IndexError, ValueError):
                    return self.get(url, False, charset)
            else:
                return self.get(url, False, charset)
        else:
            resp, content = self.http.request(url, headers={'user-agent':self.user_agent})
            self.log.debug("result content: %s response: %s fromcache: %s status: %s)" % (content, resp, str(resp.fromcache), str(resp.status)))

        c = content.decode(charset)
        return c
            


