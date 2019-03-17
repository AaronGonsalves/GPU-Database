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

class Edit(webapp2.RequestHandler):
    def get(self):
        self.response.headers['content-Type'] = 'text/html'

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        gpu_name_list_query = MyGPUDatabase().query().fetch()

        template_values = {
         'myuser' : myuser,
         'gpu_name_list_query' : gpu_name_list_query
        }

        template = JINJA_ENVIRONMENT.get_template('edit.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['content-Type'] = 'text/html'
        url_string = ''

        if self.request.get('submit') == 'Submit':

            get_gpu_name = self.request.get('gpu_name')
            get_gpu_key = ndb.Key('MyGPUDatabase', get_gpu_name)
            store_gpu_key = get_gpu_key.get()

            new_gpu_key_storing = MyGPUDatabase(id=get_gpu_name)
            new_gpu_key_storing.gpuname = self.request.get('gpu_name')
            new_gpu_key_storing.gpumanufacturing = self.request.get('gpu_manufacturing')
            new_gpu_key_storing.gpudate = datetime.strptime(self.request.get('gpu_date'), '%Y-%m-%d').date()
            new_gpu_key_storing.geometryshader = bool(self.request.get('geometryShader'))
            new_gpu_key_storing.tesselationshader = bool(self.request.get('tesselationShader'))
            new_gpu_key_storing.shaderint = bool(self.request.get('shaderInt16'))
            new_gpu_key_storing.sparsebinding = bool(self.request.get('sparseBinding'))
            new_gpu_key_storing.texturecompressionetc = bool(self.request.get('textureCompressionETC2'))
            new_gpu_key_storing.vertexpipelinestoresandatomics = bool(self.request.get('vertexPipelineStoresAndAtomics'))

            action = self.request.get('submit')
            mykey = ndb.Key('MyGPUDatabase',new_gpu_key_storing.gpuname)
            getmyuser = mykey.get()

            if getmyuser == None:
                gpu_data_store = MyGPUDatabase(id=new_gpu_key_storing.gpuname, gpuname=new_gpu_key_storing.gpuname,
                gpumanufacturing=new_gpu_key_storing.gpumanufacturing, gpudate=new_gpu_key_storing.gpudate,
                geometryshader=new_gpu_key_storing.geometryshader, tesselationshader=new_gpu_key_storing.tesselationshader,
                shaderint=new_gpu_key_storing.shaderint, sparsebinding=new_gpu_key_storing.sparsebinding,
                texturecompressionetc= new_gpu_key_storing.texturecompressionetc,
                vertexpipelinestoresandatomics=new_gpu_key_storing.vertexpipelinestoresandatomics)

                gpu_data_store.put()

                template_values = {
                    'success' : 'GPU Details added to the system'
                }
                template = JINJA_ENVIRONMENT.get_template('main.html')
                self.response.write(template.render(template_values))

            else:
                template_values = {
                    'error' : 'GPU already exist in the system'
                }
                template = JINJA_ENVIRONMENT.get_template('main.html')
                self.response.write(template.render(template_values))

        if self.request.get('button') == 'Cancel':
            self.redirect('/')
