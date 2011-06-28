#!/usr/bin/env python
import os
import codecs
import logging
import xml.etree.ElementTree as et

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

feeds = {
    'bbc'      : 'http://news.bbc.co.uk/weather/forecast/',
    'guardian' : 'http://content.guardianapis.com/search?format=json&use-date=last-modified&show-fields=headline,trailText&ids=',
    'yahoo'    : 'http://query.yahooapis.com/v1/public/yql?format=json&q='
}

api_url = 'data/xml/LM-hotels.xml'

def kapowAPI():
    return codecs.open(os.path.join(os.path.dirname(__file__), api_url))

def getRawXML():
    return kapowAPI().read()

def parseNewYork():
    results = []
    
    tree = et.parse(kapowAPI())
    for hotels in all(tree, 'object'):
        h = {}
        for hotel in all(hotels, 'attribute'):
            text = hotel.text
            name = hotel.attrib.get('name')
            h[name] = text
        
        results.append(h)
    
    logging.info(results)    
    return results

def all(element, nodename):
    """return iterable of nodes by nodename"""
    path = './/%s' % nodename
    return element.findall(path)
 
    
class RawData(webapp.RequestHandler):
    def get(self):
        raw_data = getRawXML()
        self.response.out.write(raw_data)

class Newyork(webapp.RequestHandler):
    def get(self):
        
        ny = parseNewYork()
        
        path = os.path.join(os.path.dirname(__file__),'templates/mashup.html')

        vars = {
            'name'     : 'New York',
            'bbc'      : '101',
            'news'     : feeds['guardian']+'travel/newyork',
            'weather'  : feeds['yahoo']+'select * from weather.forecast where location=10118',
        }
        self.response.out.write(template.render(path,vars))

application = webapp.WSGIApplication([
        ('/newyork/xml', RawData),
        ('/newyork',Newyork),
        ('/',Newyork)
    ],debug=True)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)
