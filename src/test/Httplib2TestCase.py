# -*- coding: utf-8 -*-
from httplib2 import Http, FileCache
import httplib2
import os
import unittest

class  Httplib2TestCase(unittest.TestCase):
    def setUp(self):
        pass
#    def tearDown(self):
#        self.epguide.dispose()
#        self.epguide = None

    def test_epgguide(self):
        cache_dir = os.getcwd() + "/.epguide"
#        os.makedirs(cache_dir)
        print cache_dir
        cache = FileCache(cache_dir)
        h = Http(cache = cache)
        user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0"
        httplib2.debuglevel = 255
        resp, content = h.request("http://www.teleman.pl/program-tv/stacje/TVP-2", headers={'user-agent':user_agent})
        print "content:"
        print content
        print "response:"
        print resp
        print "fromcache:" + str(resp.fromcache)
        print "status:" + str(resp.status)
        #url = "http://www.teleman.pl/program-tv/stacje/TVP-2"
        url = "http://www.teleman.pl/tv/Dr-House-7-152-885990"
        resp, content = h.request(url, headers={'user-agent':user_agent})
        print "fromcache:" + str(resp.fromcache)
        print "status:" + str(resp.status)
        safe = httplib2.safename(url)
        print "safe:" + safe
        cached_value = cache.get(url)
        info, cached = cached_value.split('\r\n\r\n', 1)
        print "===="
        print content
        print "===="
        print cached
        print "===="
        self.assertEqual(content, cached)

if __name__ == '__main__':
    unittest.main()

