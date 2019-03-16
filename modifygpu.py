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

class ModifyEdit(webapp2.RequestHandler):
    def get(self):
        self.response.headers['content-Type'] = 'text/html'

        gpu_name_clicked = self.request.GET.get("gpu_name_list_display")
        gpu_name_clicked_key = ndb.Key("MyGPUDatabase", gpu_name_clicked)
        clicked_gpuname_key = gpu_name_clicked_key.get()

        template_values = {
            "clicked_gpu_name" : gpu_name_clicked,
            "clicked_gpuname_key" : clicked_gpuname_key
        }

        template = JINJA_ENVIRONMENT.get_template("modifygpu.html")
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers["Content-Type"] = "text/html"

        if self.request.get("update") == "Update":

            user_clicked_gpuname = self.request.get("gpu_name_update")
            user_clicked_gpuname_key = ndb.Key("MyGPUDatabase", user_clicked_gpuname)
            clicked_gpuname_key = user_clicked_gpuname_key.get()

            gpu_name_update_store = self.request.get("gpu_name_update")
            gpu_manufacturing_update_store = self.request.get("gpu_manufacturing_update")
            gpu_date_update_store = datetime.strptime(self.request.get("gpu_date_update"),'%Y-%m-%d').date()
            geometryShader_update_store = bool(self.request.get("geometryShader_update"))
            tesselationShader_update_store = bool(self.request.get("tesselationShader_update"))
            shaderInt16_update_store = bool(self.request.get("shaderInt16_update"))
            sparseBinding_update = bool(self.request.get("sparseBinding_update"))
            textureCompressionETC2_update_store = bool(self.request.get("textureCompressionETC2_update"))
            vertexPipelineStoresAndAtomics_update_store = bool(self.request.get("vertexPipelineStoresAndAtomics_update"))

            clicked_gpuname_key.gpumanufacturing = gpu_manufacturing_update_store
            clicked_gpuname_key.gpudate = gpu_date_update_store
            clicked_gpuname_key.geometryshader = geometryShader_update_store
            clicked_gpuname_key.tesselationshader = tesselationShader_update_store
            clicked_gpuname_key.shaderint = shaderInt16_update_store
            clicked_gpuname_key.sparsebinding = sparseBinding_update
            clicked_gpuname_key.texturecompressionetc = textureCompressionETC2_update_store
            clicked_gpuname_key.vertexpipelinestoresandatomics = vertexPipelineStoresAndAtomics_update_store

            clicked_gpuname_key.put()
            self.redirect("/edit")

        elif self.request.get('button') == 'Cancel':
            self.redirect('/edit')
