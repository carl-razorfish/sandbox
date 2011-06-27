#!/usr/bin/env python
import os
import codecs
import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

feeds = {
    'bbc'      : 'http://news.bbc.co.uk/weather/forecast/',
    'guardian' : 'http://content.guardianapis.com/search?format=json&use-date=last-modified&show-fields=headline,trailText&ids=',
    'yahoo'    : 'http://query.yahooapis.com/v1/public/yql?format=json&q='
}

api_url = 'data/xml/LM-hotels.xml'

def getRawXML():
    f = codecs.open(os.path.join(os.path.dirname(__file__), api_url))
    return f.read()
    
class RawData(webapp.RequestHandler):
    def get(self):
        raw_data = getRawXML()
        self.response.out.write(raw_data)

class Newyork(webapp.RequestHandler):
    def get(self):
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
        ('/',Newyork)
    ],debug=True)

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)
