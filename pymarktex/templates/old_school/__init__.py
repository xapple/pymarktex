# Internal modules #
from pymarktex import logo_dir
from pymarktex.templates import Template

# First party modules #
from autopaths.file_path import FilePath

###############################################################################
class HeaderTemplate(Template):
    """All the parameters to be rendered in the LaTeX header template"""
    def name(self):        return self.option_or_empty('name')
    def status(self):      return self.option_or_empty('status', ', ')
    def company(self):     return self.option_or_empty('company')
    def subcompany(self):  return self.option_or_empty('subcompany')
    def title(self):       return self.option_or_empty('title')

    def option_or_empty(self, name, prefix=None):
        result = self.options.get(name)
        if result is None: return ""
        if prefix is not None: return prefix + result
        return result

    def image_path(self):
        # Get the option #
        result = self.options.get('image_path')
        # If it's a path #
        if isinstance(result, FilePath): return result.unix_style
        # If it's a string #
        if isinstance(result, str): return (logo_dir + result).unix_style

###############################################################################
class FooterTemplate(Template):
    """All the parameters to be rendered in the LaTeX footer template"""
    pass