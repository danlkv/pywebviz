from setuptools import setup
setup(
      name = 'pywebvis',
      packages = ['webvis',
                 ],
      version = '0.0.1',
      description = 'A live two-way data binder for python',
      author = 'Danil Lykov',
      author_email = 'lkvdan@gmail.com',
      url = 'https://github.com/DaniloZZZ/pywebvis',
      install_requires=['matplotlib', 'numpy', 'requests',
          'mpld3','trio','trio-websocket'],
      python_requires='>=3.3',
      license='MIT',
      keywords = ['tools', 'data', 'framework', 'visualization'], # arbitrary keywords
      classifiers = [],
)