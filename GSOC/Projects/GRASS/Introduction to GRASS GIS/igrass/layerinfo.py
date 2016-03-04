import grass.script as grass
from IPython.core.display import HTML

def dict2html(dic, keys=None, border='', prec=4):
    dcont = """<tr>
    <td><b>%s</b></td>
    <td>%s</td>
    </tr>"""
    keys = keys if keys else sorted(dic.keys())
    header = "<table border=%r>" % border if border else "<table>"    
    content = [dcont % (k,dic[k]) for k in keys]
    return '\n'.join([header, ] + content + ['</table>', ])

def list2dict(inputlist, sep="=", inverse=False):
    if inverse:
        dictionary = dict([(i.split(sep)[1],i.split(sep)[0]) for i in inputlist])
    else :
        dictionary = dict([(i.split(sep)[0],i.split(sep)[1]) for i in inputlist])
    return dictionary

def rlayerInfo(map):
    raster_info = grass.read_command('r.info', map=map, flags='g').strip().split('\n')
    raster_info = list2dict(raster_info)
    
    map_range = grass.read_command('r.info', map=map, flags='r').strip().split('\n')
    map_range = list2dict(map_range)
    raster_info['range'] = map_range
    return raster_info

def vlayerInfo(map,layer=1):
    hist = grass.read_command('v.info', map=map, layer=1, flags='h').split('\n')
    map_history = {'COMMAND' : hist[0].split(':')[1],
                   'GISDBASE' : hist[1].split(':')[1],
                   'LOCATION' : hist[2].split(' ')[1],
                   'MAPSET' : hist[2].split(' ')[3],
                   'USER' : hist[2].split(' ')[5],
                   'DATE' : hist[2].split(' ')[7:]}
    map_table = grass.read_command('v.info', map=map, layer=1, flags='c').strip().split('\n')
    map_table = list2dict(map_table[1:], sep='|', inverse=True)
    map_region = grass.read_command('v.info', map=map, layer=1, flags='g').strip().split('\n')
    map_region = list2dict(map_region)
    map_topology = grass.read_command('v.info', map=map, layer=1, flags='t').strip().split('\n')
    map_topology = list2dict(map_topology)
    info = {'table' : map_table,
            'region' : map_region,
            'history' : map_history,
            'topology' : map_topology,
            } #'title' : map_title
    return info