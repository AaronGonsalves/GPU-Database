import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from datetime import datetime
from myuser import MyUser
from mygpudatastore import MyGPUDatabase

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class CompareGPUDisplay(webapp2.RequestHandler):

    def get(self):

        self.response.headers['content-Type'] = 'text/html'

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        selected_gpu_name = self.request.get("selected_gpuname_listed")
        gpuname_already_listed = self.request.get("gpuname_listed")

        if selected_gpu_name != None and gpuname_already_listed != None:

            gpu_name_list_compare_query = MyGPUDatabase.query(ndb.OR(MyGPUDatabase.gpuname == selected_gpu_name, MyGPUDatabase.gpuname == gpuname_already_listed)).fetch()

        else:
            gpu_name_list_compare_query = MyGPUDatabase().query().fetch()

        template_values = {
         'myuser' : myuser,
         'gpu_name_list_query' : gpu_name_list_compare_query
        }

        if self.request.get("cancel"):
            self.redirect("/")

        template = JINJA_ENVIRONMENT.get_template('comparegpu.html')
        self.response.write(template.render(template_values))

    def post(self):

        self.response.headers['content-Type'] = 'text/html'
