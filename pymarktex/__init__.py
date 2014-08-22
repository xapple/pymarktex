b"""This module needs Python 2.7.x"""

# Special variables #
__version__ = '1.0.1'

# Built-in modules #
import os, sys

# Get paths to module #
self = sys.modules[__name__]
module_dir = os.path.dirname(self.__file__)
repos_dir = os.path.abspath(module_dir + '/../') + '/'

# Various paths #
logo_dir = repos_dir + 'logos/'
template_dir = repos_dir + 'templates/'