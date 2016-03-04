import os
import tempfile

from IPython.core.display import Image, HTML, display_html, display

from grass.script import core as gcore
from grass.pygrass.modules.shortcuts import display as d
from grass.pygrass.modules.shortcuts import general as g

from corner import llcorner
import uuid


def dict2html(dic, keys=None, border='', prec=4):
    dcont = """    <tr>
    <td><b>{key}</b></td>
    <td>{value}</td>
    </tr>"""
    keys = keys if keys else sorted(dic.keys())
    header = "<table border=%r>" % border if border else "<table>"
    content = [dcont.format(key=k, value=(round(dic[k][0],prec),round(dic[k][1],prec)) ) for k in keys]
    return display_html(HTML('\n'.join([header, ] + content + ['</table>', ])))


def view(rasters=None, vectors=None,
         pngfile=None, width=640, height=480,
         transparent=True, read_file=True, truecolor=True,
         engine='cairo', compression=9, rkw=None, vkw=None, corner=False, meta=False):
    """Return an IPython image object rendered by GRASS GIS.
    Parameters
    -----------
    rasters: list
        List with the raster map name to be rendered
    vectors: list
        List with the vector map name to be rendered
    pngfile: path
        Path to the PNG file, default creates a temporary file
    width: int
        Width size of the image
    height: int
        Height size of the image
    """

    def gdisplay():
        for raster in rasters if rasters else []:
            d.rast(map=raster, **(rkw if rkw else {}))
        for vector in vectors if vectors else []:
            d.vect(map=vector, **(vkw if vkw else {}))
    
    unique_filename = uuid.uuid4()
    pngfile = str(unique_filename.int)+'.png'
    bounds = llcorner().corners
    if corner:
        dict2html(bounds)
    # set the enviornmental variables
    os.environ['GRASS_RENDER_IMMEDIATE'] = engine
    os.environ['GRASS_RENDER_FILE'] = pngfile
    os.environ['GRASS_RENDER_FILE_COMPRESSION'] = str(compression)
    os.environ['GRASS_RENDER_WIDTH'] = str(width)
    os.environ['GRASS_RENDER_HEIGHT'] = str(height)
    os.environ['GRASS_RENDER_TRANSPARENT'] = 'TRUE' if transparent else None
    os.environ['GRASS_RENDER_READ_FILE'] = 'TRUE' if read_file else None
    os.environ['GRASS_RENDER_TRUECOLOR'] = 'TRUE' if truecolor else None
    os.environ['GRASS_RENDER_PNG_AUTO_WRITE'] = 'TRUE'

    monitor = gcore.gisenv().get('MONITOR', None)
    if monitor:
        g.gisenv(unset='MONITOR')
        gdisplay()
        g.gisenv(set='MONITOR=%s' % monitor)
    else:
        gdisplay()
    if meta:
        metadata={'corners': bounds, 'filename': pngfile, 'raster':rasters, 'vector':vectors}
    if not meta:
        metadata=None
    return display(Image(pngfile),metadata=metadata) 