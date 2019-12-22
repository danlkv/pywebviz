import json
import numpy as np
from webvis.VisVars import VisVars
try:
    import matplotlib
    import mpld3
    #mpld3 hack
    class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            import numpy as np
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            return json.JSONEncoder.default(self, obj)
    from mpld3 import _display
    _display.NumpyEncoder = NumpyEncoder
    import bokeh
except Exception as e:
    print(e)

def is_mpl(val):
    try:
        return isinstance(val, matplotlib.figure.Figure)
    except Exception as e:
        return False
def is_bokeh(val):
    try:
        return isinstance(val,bokeh.model.Model) or isinstance(val,bokeh.document.document.Document)
    except Exception as e:
        return False

def preprocess_value(val):
    if is_bokeh(val):
        ret = bokeh.embed.file_html(val, bokeh.resources.Resources('cdn'))
        type_ = 'mpl'
    elif is_mpl(val):
        ret = mpld3.fig_to_html(val)
        type_ = 'mpl'
    elif type(val)==np.ndarray:
        ret, type_ = ndarray_val(val)
    elif isinstance(val, VisVars):
        ret, type_ = vismodule_val(val)
    else:
        ret = val
        type_ = 'raw'

    return ret, type_

def vismodule_val(val):
    ret = val.ref()
    type_ = val.name
    return ret, type_

def ndarray_val(val):
    sh = val.shape
    ret = None
    if len(sh) >= 2:
        if sh[0]>10 and sh[1]>10:
            ret = numpy_to_image(val)
            type_='img'
        else:
            ret = val.tolist()
            type_ = 'raw'
    else:
        ret = val.tolist()
        type_ = 'raw'
    return ret, type_

def numpy_to_image(val):
    sh = val.shape
    alpha = np.ones(list(sh[:2])+[1])*255
    if len(sh)==2:
        # Grayscale image
        val = val.reshape(sh[0],-1,1)
        val = np.concatenate((val,val,val,alpha),axis = -1)
    if len(sh)==3:
        # Color image
        val = np.concatenate((val,alpha), axis=-1)
    val = val.flatten()
    ret = list(sh[:2]) + val.tolist()
    return ret

## ## Depr

def convert_val(val):
    if is_bokeh(val):
        ret = bokeh.embed.file_html(val, bokeh.resources.Resources('cdn'))
        type_ = 'mpl'
    elif is_mpl(val):
        ret = mpld3.fig_to_html(val)
        type_ = 'mpl'
    elif type(val)==np.ndarray:
        sh = val.shape
        if len(sh) >= 2:
            if sh[0]>10 and sh[1]>10:
                alpha = np.ones(list(sh[:2])+[1])*255
                if len(sh)==2:
                    val = val.reshape(sh[0],-1,1)
                    val = np.concatenate((val,val,val,alpha),axis = -1)
                if len(sh)==3:
                    val = np.concatenate((val,alpha), axis=-1)
                val = val.flatten()
                ret = list(sh[:2]) + val.tolist()
                type_='img'
