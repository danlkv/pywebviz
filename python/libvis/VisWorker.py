import webbrowser
from legimens import App

from libvis import ref
from .helpers.threaded import threaded
from .http_server import create_server as create_http
from .VisVars import VisVars, VisObject
from .interface import add_serializer, serialize_to_vis

class Vis():
    def __init__(self, ws_port = 7700, vis_port=7000, nb_name=None):
        self.ws_port = ws_port
        self.vis_port = vis_port
        self.nb_name = nb_name

        self.http_server = create_http(port=vis_port)

        self.app = App(addr='localhost', port=ws_port)
        self.app.vars = VisVars()
        self.app._register_child(self.app.vars)
        self.app.serialize_value = serialize_to_vis
        self.vars = self.app.vars

    def use(type_, serializer):
        add_serializer(type_, serializer)

    def watch(self, obj, key, serializer=None):
        o = VisObject(obj)
        self.app.watch_obj(o)
        self.vars[key] = o
        if serializer:
            # Note: this will act on *any* object of the same type
            self.use(type(obj), serializer)
        return ref(o)

    def start(self):
        if self.http_server is None:
            raise Exception("http server not initialized. Recreate Vis instance.")
        self.phttp = threaded( self.http_server.serve_forever, name='http')
        self.app.run()

    def show(self):
        if self.nb_name:
            params = '?p='+self.nb_name
        else: params = ''
        webbrowser.open_new_tab(
            f"http://localhost:{self.vis_port}/{params}"
        )

    def stop(self):
        print("Stopping app server")
        if hasattr(self, 'phttp'):
            if self.phttp.is_alive():
                self.http_server.shutdown()
        else:
            print('Warning: http was already dead')
        print("Stopping websocket server")
        self.app.stop()
