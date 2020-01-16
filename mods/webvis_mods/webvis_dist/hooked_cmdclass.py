from distutils.command.install import install as install_orig
from distutils.errors import DistutilsExecError

from setuptools import setup

noop = lambda *x, **y: None

def get_class(orig, pre=noop, post=noop):
    class hooked_distutils_class(orig):
        def __init__(self, *args, 
                     **kwargs):
            super().__init__(*args, **kwargs)
            self.webvis_pre_hook = pre
            self.webvis_post_hook = post

        def run(self):
            self.webvis_pre_hook()
            super().run()
            self.webvis_post_hook()

    return hooked_distutils_class
