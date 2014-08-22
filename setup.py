from distutils.core import setup

with open('README.md') as readme:
        long_description = readme.read()

setup(
        name             = 'pymarktex',
        version          = '1.0.1',
        description      = 'Will convert a markdown text file to a fancy PDF document',
        long_description = long_description,
        license          = 'MIT',
        url              = 'http://github.com/xapple/pymarktex/',
        author           = 'Lucas Sinclair',
        author_email     = 'lucas.sinclair@me.com',
        install_requires = ['sh', 'pystache'],
    )
