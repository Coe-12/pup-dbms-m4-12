import webapp2
from google.appengine.ext import ndb
import jinja2
import os
import logging
import json
import urllib
from google.appengine.api import users



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)

class Thesis(ndb.Model):
    year = ndb.StringProperty(indexed=True)
    thesisTitle = ndb.StringProperty(indexed=True)
    abstract = ndb.StringProperty(indexed=True)
    adviser = ndb.StringProperty(indexed=True)
    section = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)
    userName = ndb.StringProperty(indexed=False)
    userId = ndb.StringProperty(indexed=False)

class CreateThesis(webapp2.RequestHandler):
    #def get(self):
     #   template = JINJA_ENVIRONMENT.get_template('main.html')
      #  self.response.write(template.render())
    def get(self):
        #get all student
        thesis = Thesis.query().order(-Thesis.date).fetch()
        thesis_list = []

        for t in thesis:
            thesis_list.append({
                    'year' : t.year,
                    'thesisTitle' : t.thesisTitle,
                    'abstract' : t.abstract,
                    'adviser' : t.adviser,
                    'section' : t.section,
                    'id' : t.key.id(),
                    'userName' : t.userName
                })
        #return list to client
        response = {
            'result' : 'OK',
            'data' : thesis_list
        }
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(response))

    def post(self):
        user = users.get_current_user()
        t = Thesis()
        t.thesisTitle = self.request.get('thesisTitle')
        t.abstract = self.request.get('abstract')
        t.adviser = self.request.get('adviser')
        t.year = self.request.get('year')
        t.section = self.request.get('section')
        t.userName = user.nickname()
        t.userId = user.user_id()
        t.put()

        self.response.headers['Content-Type'] = 'application/json'
        response = {
            'result' : 'OK',
            'data': {
                'year' : t.year,
                'thesisTitle' : t.thesisTitle,
                'abstract' : t.abstract,
                'adviser' : t.adviser,
                'section' : t.section,
                'id' : t.key.id(),
                'userName' : t.userName
            }
        }
        self.response.out.write(json.dumps(response))

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        url = users.create_logout_url(self.request.uri)
        url_linktext = 'Logout'

        template_data = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext
        }
        if user:
            template = JINJA_ENVIRONMENT.get_template('main.html')
            self.response.write(template.render(template_data))
        else:
            self.redirect(users.create_login_url(self.request.uri))

class deleteThesis(webapp2.RequestHandler):
    def get(self, thesisId):
        d = Thesis.get_by_id(int(thesisId))
        d.key.delete()
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/home', MainPageHandler),
    ('/', MainPageHandler),
    ('/api/thesis', CreateThesis),
    ('/thesis/delete/(.*)', deleteThesis)
], debug=True)