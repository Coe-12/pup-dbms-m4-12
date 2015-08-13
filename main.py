import webapp2
from google.appengine.ext import ndb
import jinja2
import os
import logging
import json
import urllib



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Thesis(ndb.Model):
    year = ndb.IntegerProperty()
    thesisTitle = ndb.StringProperty(indexed=True)
    abstract = ndb.StringProperty(indexed=True)
    adviser = ndb.StringProperty(indexed=True)
    section = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class CreateThesis(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render())

    def post(self):
        thesis = Thesis()
        thesis.thesisTitle = self.request.get('thesisTitle')
        thesis.abstract = self.request.get('abstract')
        thesis.adviser = self.request.get('adviser')
        thesis.year = int(self.request.get('year'))
        thesis.section = int(self.request.get('section'))
        thesis.put()

        #student.first_name = self.request.get('first_name')
        #student.last_name = self.request.get('last_name')
        #student.age = int(self.request.get('age'))
        #student.put()

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render())


app = webapp2.WSGIApplication([
    ('/home', MainPageHandler),
    ('/', MainPageHandler),
    ('/api/thesis', CreateThesis)
], debug=True)