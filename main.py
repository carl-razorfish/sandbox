#!/usr/bin/env python
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class Newyork(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__),'templates/mashup.html')
        vars = {
            'name'     : 'New York',
            'bbc'      : '101',
            'guardian' : 'travel/newyork'
        }
        self.response.out.write(template.render(path,vars))

application = webapp.WSGIApplication([
        ('/',Newyork)
    ],debug=True)

if __name__ == '__main__':
    run_wsgi_app(application)
