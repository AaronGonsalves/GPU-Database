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

class UpdateEdit(webapp2.RequestHandler):
    def get(self):
        self.response.headers['content-Type'] = 'text/html'

        gpu_name_clicked = self.request.GET.get("gpu_name_list_display")
        gpu_name_clicked_key = ndb.Key("MyGPUDatabase", gpu_name_clicked)
        clicked_gpuname_key = gpu_name_clicked_key.get()

        template_values = {
            "clicked_gpu_name" : gpu_name_clicked,
            "clicked_gpuname_key" : clicked_gpuname_key
        }

        template = JINJA_ENVIRONMENT.get_template("updateedit.html")
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers["Content-Type"] = "text/html"

        if self.request.get('button') == 'Cancel':
            self.redirect('/edit')
