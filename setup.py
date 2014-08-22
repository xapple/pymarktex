from distutils.core import setup

setup(
        name             = 'pymarktex',
        version          = '1.0.2',
        description      = 'Will convert a markdown text file to a fancy PDF document',
        long_description = open('README.md').read(),
        license          = 'MIT',
        url              = 'http://github.com/xapple/pymarktex/',
        author           = 'Lucas Sinclair',
        author_email     = 'lucas.sinclair@me.com',
        install_requires = ['sh', 'pystache'],
    )
