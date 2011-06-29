#!/usr/bin/env python
import re
import os
import codecs
import logging
import xml.etree.ElementTree as et

from django.utils import simplejson as json

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

feeds = {
    'bbc'      : 'http://news.bbc.co.uk/weather/forecast/',
    'guardian' : 'http://content.guardianapis.com/search?format=json&use-date=last-modified&show-fields=headline,trailText&ids=',
    'yahoo'    : 'http://query.yahooapis.com/v1/public/yql?format=json&q='
}

ny_hotels_feed = 'data/xml/LM-hotels.xml'
ny_city_breaks_feed = 'data/xml/LM-city-breaks.xml'

ny_mashup = {
    'name'     : 'New York',
    'bbc'      : '101',
    'news'     : feeds['guardian']+'travel/newyork',
    'weather'  : feeds['yahoo']+'select * from weather.forecast where location=10118'
}

def kapowAPI(request):
    return codecs.open(os.path.join(os.path.dirname(__file__), request))

def getXML(request):
    return kapowAPI(request).read()

def getJSON(request):
    return json.dumps(parseXML(request))

def parseXML(request):
    results = []
    tree = et.parse(kapowAPI(request))
    for items in all(tree, 'object'):
        i = {}
        for item in all(items, 'attribute'):
            text = item.text
            name = item.attrib.get('name')
            i[name] = text

        results.append(i)
    return results

def split_path(path):
    p = re.compile('\W+')
    return p.split(path)

def all(element, nodename):
    path = './/%s' % nodename
    return element.findall(path)

class RestAPI(webapp.RequestHandler):
    def get(self):
        
        r = split_path(self.request.path)
         
        if r[1] == 'newyork':
            feed = ny_hotels_feed
        
        if r[2] == 'json':
            out = getJSON(feed)
        elif r[2] == 'xml':
            out = getXML(feed)
        
        self.response.out.write(out)

class Mashup(webapp.RequestHandler):
    def get(self):
        
        r = split_path(self.request.path)
        
        if r[1] == '' or r[1] == 'newyork':
            mashup = ny_mashup
            hotels_feed = ny_hotels_feed
            city_breaks_feed = ny_city_breaks_feed
        
        mashup['hotels'] = parseXML(hotels_feed);
        mashup['city_break'] = parseXML(city_breaks_feed)[0]
        
        logging.info(mashup['city_break'])
        
        path = os.path.join(os.path.dirname(__file__),'templates/mashup.html')
        self.response.out.write(template.render(path, ny_mashup))

application = webapp.WSGIApplication([
        ('/newyork/xml', RestAPI),
        ('/newyork/json', RestAPI),
        ('/newyork',Mashup),
        ('/',Mashup)
    ],debug=True)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)
