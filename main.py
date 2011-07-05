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

requestRestApi = r"/(.*)/(xml|json)"
requestUI = r"/(.*)"

feeds = {
    'bbc'      : 'http://news.bbc.co.uk/weather/forecast/',
    'guardian' : 'http://content.guardianapis.com/search?format=json&use-date=last-modified&show-fields=headline,trailText&ids=',
    'yahoo'    : 'http://query.yahooapis.com/v1/public/yql?format=json&q='
}

ny_hotels_feed = 'data/xml/LM-hotels.xml'
ny_city_breaks_feed = 'data/xml/LM-city-breaks.xml'
ny_flights_feed = 'data/xml/lastminute.xml'

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
    def get(self, destination, responseType):
        logging.info(destination)
        logging.info(responseType)
        feed = None 
        if destination == 'newyork':
            feed = ny_hotels_feed
        if feed is not None:
	        if responseType == 'json':
	            out = getJSON(feed)
	        elif responseType == 'xml':
	   			out = getXML(feed)
	        if out is not None:
	        	self.response.out.write(out)

class Mashup(webapp.RequestHandler):
    def get(self, destination):
        r = split_path(self.request.path)
        flights_feed = None
        hotels_feed = None
        city_breaks_feed = None
        mashup = None
        f = None

        if r[1] == '' or r[1] == 'newyork':
            mashup = ny_mashup
            hotels_feed = ny_hotels_feed
            city_breaks_feed = ny_city_breaks_feed
            flights_feed = ny_flights_feed
        if flights_feed is not None:
        	f = parseXML(flights_feed)
        if hotels_feed is not None:
        	mashup['hotels'] = parseXML(hotels_feed)
		if city_breaks_feed is not None:
			mashup['city_break'] = parseXML(city_breaks_feed)[0]
		if f is not None:
			mashup['cheapest_flight'] = f[-1]
        	mashup['all_flights'] = f[0:-2]
        if mashup is not None:
			logging.info(mashup['all_flights'])
        
        path = os.path.join(os.path.dirname(__file__),'templates/mashup.html')
        self.response.out.write(template.render(path, mashup))

application = webapp.WSGIApplication([
        (requestRestApi, RestAPI),
        (requestUI,Mashup)
    ],debug=True)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)
