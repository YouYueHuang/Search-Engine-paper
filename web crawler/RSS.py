# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 13:21:39 2017

@author: yhuang
"""
import feedparser
d = feedparser.parse('https://news.google.com/news?cf=all&hl=en&ned=us&topic=tc&output=rss')
print d['feed']['title']
print d['feed']['link']
print d.feed.subtitle
print len(d['entries'])

print d['entries'][0]['title'] 
print d.entries[0]['link']

for post in d.entries:
    print post.title + ": " + post.link
    
print d.version 
print d.headers      
print d.headers.get('content-type')

print d["channel"]["title"]
print d["channel"]["description"]
print d["channel"]["link"]
#print d["channel"]["wiki_interwiki"]
print d["items"]