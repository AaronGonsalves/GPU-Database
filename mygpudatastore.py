from google.appengine.ext import ndb

class MyGPUDatabase(ndb.Model):
    gpuname = ndb.StringProperty()
    gpumanufacturing = ndb.StringProperty()
    gpudate = ndb.DateProperty()
    geometryshader = ndb.BooleanProperty()
    tesselationshader = ndb.BooleanProperty()
    shaderint = ndb.BooleanProperty()
    sparsebinding = ndb.BooleanProperty()
    texturecompressionetc = ndb.BooleanProperty()
    vertexpipelinestoresandatomics = ndb.BooleanProperty()
