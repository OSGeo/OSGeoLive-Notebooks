from grass.pygrass.gis import region
import grass.script as grass
import pyproj
from IPython.core.display import display, Javascript, HTML

import ctypes
import grass.lib.gis as libgis
from grass.pygrass.errors import GrassError

class llcorner(region.Region):
    def __init__(self, reg=region.Region(),default=False, prec=4, meta=None):
        self.c_region = ctypes.pointer(libgis.Cell_head())
        self.corners = self.llcorner(reg)
        self.prec = prec
        self.meta = meta
        if default:
            self.get_default()
        else:
            self.get_current()
            
    def dict2html(self, dic, keys=None, border='', prec=4):
        dcont = """    <tr>
          <td><b>{key}</b></td>
          <td>{value}</td>
        </tr>"""
        keys = keys if keys else sorted(dic.keys())
        header = "<table border=%r>" % border if border else "<table>"
        content = [dcont.format(key=k, value=(round(float(dic[k][0]),prec),round(dic[k][1],prec))) for k in keys]
        return '\n'.join([header, ] + content + ['</table>', ])

    
    def llcorner(self, reg, prj=None):
        if not prj:
            prj = grass.read_command('g.proj', flags='j').replace('\n',' ')  
        p1 = pyproj.Proj(prj)
        corners = {'ul': p1(reg.east,reg.north, inverse=True),
                  'ur' : p1(reg.west,reg.north, inverse=True),
                  'lr' : p1(reg.west,reg.south, inverse=True),
                  'll' : p1(reg.east,reg.south, inverse=True)}
        return corners    
    
    def get_default(self):
        """Set the default GRASS region to the Region object"""
        libgis.G_get_window(self.c_region)

    def set_default(self):
        """Set the Region object to the default GRASS region.
        It works only in PERMANENT mapset"""
        from grass.pygrass.gis import Mapset
        mapset = Mapset()
        if mapset.name != 'PERMANENT':
            raise GrassError("ERROR: Unable to change default region. The " \
                             "current mapset is not <PERMANENT>.")
        self.adjust()
        if libgis.G_put_window(self.c_region) < 0:
            raise GrassError("Cannot change region (DEFAUL_WIND file).")    

    @property
    def addmeta(self):
        display('cell output metadata: corners, region', metadata={'corners': self.corners, 'region': dict(self.items())})
        #return self.corners
    
    @property
    def ul(self):
        #display('upper left', metadata={'prov': self.corners['ul']})
        return self.corners['ul']
    
    @property
    def ur(self):
        return self.corners['ur']
    @property
    def lr(self):
        return self.corners['lr']
    
    @property
    def ll(self):
        return self.corners['ll']
    
    
    def __repr__(self):
        return str(self.corners)

    def _repr_html_(self,meta='None'):
        if self.meta:
            display("region corners: (Longitude, Latitude)", metadata={'corners': self.corners, 'region': dict(self.items())})
        return self.dict2html(dict(self.corners.items()), keys=self.corners.keys(), border='1', prec=self.prec)