# -*- coding: utf-8 -*-
'''
Created on 25-02-2013

@author: Damian
'''

from httplib2 import Http, FileCache
import httplib2
import os
import logging

class HttpHelper(object):
    '''
    classdocs
    '''

    def __init__(self, enable_debug):
        self.log = logging.getLogger("epguide")
        cache_dir = os.path.normpath(os.path.expanduser("~/.epguide/cache"))
        self.log.debug("Cache dir: " + cache_dir)
        self.cache = FileCache(cache_dir)
        self.http = Http(cache = self.cache)
        self.user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0"
        if(enable_debug):
            httplib2.debuglevel = 255
        
    def get(self, url, force_cache = False):
        if(force_cache):
            cached_value = self.cache.get(url)
            if cached_value:
                try:
                    info, content = cached_value.split('\r\n\r\n', 1)
                    if(content):
                        return content.decode("UTF-8")
                    else:
                        return self.get(url, False)
                except (IndexError, ValueError):
                    return self.get(url, False)
            else:
                return self.get(url, False)
        else:
            resp, content = self.http.request(url, headers={'user-agent':self.user_agent})
            self.log.debug("result content: %s response: %s fromcache: %s status: %s)" % (content, resp, str(resp.fromcache), str(resp.status)))

        c = content.decode("UTF-8")
        return c
            


