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

class SearchGPU(webapp2.RequestHandler):

    def get(self):
        self.response.headers['content-Type'] = 'text/html'

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()

        geometryshader = False
        tesselationshader = False
        shaderint = False
        sparsebinding = False
        texturecompressionetc = False
        vertexpipelinestoresandatomics = False
        listGPUDetails_query = ''

        if self.request.get("searchinggpu") == "Search":

            geometryshader = bool(self.request.get("geometryShader_Search"))
            tesselationshader = bool(self.request.get("tesselationShader_Search"))
            shaderint = bool(self.request.get("shaderInt16_Search"))
            sparsebinding = bool(self.request.get("sparseBinding_Search"))
            texturecompressionetc = bool(self.request.get("textureCompressionETC2_Search"))
            vertexpipelinestoresandatomics = bool(self.request.get("vertexPipelineStoresAndAtomics_Search"))

            listGPUDetails = MyGPUDatabase.query()

            if geometryshader == True:
                listGPUDetails = listGPUDetails.filter(MyGPUDatabase.geometryshader == True)
            if tesselationshader == True:
                listGPUDetails = listGPUDetails.filter(MyGPUDatabase.tesselationshader == True)
            if shaderint == True:
                listGPUDetails = listGPUDetails.filter(MyGPUDatabase.shaderint == True)
            if sparsebinding == True:
                listGPUDetails = listGPUDetails.filter(MyGPUDatabase.sparsebinding == True)
            if texturecompressionetc == True:
                listGPUDetails = listGPUDetails.filter(MyGPUDatabase.texturecompressionetc == True)
            if vertexpipelinestoresandatomics == True:
                listGPUDetails = listGPUDetails.filter(MyGPUDatabase.vertexpipelinestoresandatomics == True)

            listGPUDetails_query = listGPUDetails.fetch()

        template_values = {
         'myuser' : myuser,
         'geometryShader_Search' : geometryshader,
         'tesselationShader_Search' : tesselationshader,
         'shaderInt16_Search' : shaderint,
         'sparseBinding_Search' : sparsebinding,
         'textureCompressionETC2_Search' : texturecompressionetc,
         'vertexPipelineStoresAndAtomics_Search' : vertexpipelinestoresandatomics,
         'listGPUDetails_query_list' : listGPUDetails_query
        }

        template = JINJA_ENVIRONMENT.get_template('searchgpu.html')
        self.response.write(template.render(template_values))

    def post(self):

        self.response.headers["Content-Type"] = "text/html"

        if self.request.get('button') == 'Cancel':
            self.redirect('/')
