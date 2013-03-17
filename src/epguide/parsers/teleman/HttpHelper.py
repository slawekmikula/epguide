# -*- coding: utf-8 -*-
'''
Created on 25-02-2013

@author: Damian
'''

from httplib2 import Http, FileCache
import httplib2
import os

class HttpHelper(object):
    '''
    classdocs
    '''


    def __init__(self, enable_debug):
        cache_dir = os.getcwd() + "/.epguide"
#        os.makedirs(cache_dir)
        print cache_dir
        self.cache = FileCache(cache_dir)
        self.http = Http(cache = self.cache)
        self.user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0"
        if(enable_debug):
            httplib2.debuglevel = 255
        
    def get(self, url, force_cache = False):
        if(force_cache):
            content = self.cache.get(url)
            if(content):
                return content
            else:
                return self.get(url, False)
        else:
            resp, content = self.http.request(url, headers={'user-agent':self.user_agent})
            print "content:"
            print content
            print "response:"
            print resp
            print "fromcache:" + str(resp.fromcache)
            print "status:" + str(resp.status)

        c = content.decode("UTF-8")
        return c
            


