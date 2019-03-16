import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from myuser import MyUser
from edit import Edit
from updateedit import UpdateEdit
from searchgpu import SearchGPU
from mygpudatastore import MyGPUDatabase
from comparegpu import CompareGPUDisplay
from modifygpu import ModifyEdit
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['content-Type'] = 'text/html'
        url = ''
        url_string = ''
        welcome = 'Welcome'
        myuser = None

        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'Logout'

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            if myuser == None:
                welcome = 'Welcome to the application'
                myuser = MyUser(id=user.user_id())
                myuser.put()
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'Login'

        gpu_name_list_compare_query = MyGPUDatabase().query().fetch()

        template_values = {
         'url' : url,
         'url_string' : url_string,
         'user' : user,
         'welcome' : welcome,
         'myuser' : myuser,
         'gpu_name_list_query' : gpu_name_list_compare_query
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/',MainPage),
    ('/edit',Edit),
    ('/updateedit',UpdateEdit),
    ('/searchgpu',SearchGPU),
    ('/comparegpu', CompareGPUDisplay),
    ('/modifygpu', ModifyEdit)
    ], debug=True)
