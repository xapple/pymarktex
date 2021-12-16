# Internal modules #
from pymarktex.templates import Template

###############################################################################
class HeaderTemplate(Template):
    """All the parameters to be rendered in the LaTeX header template"""
    def name(self):        return self.options.get('name')
    def status(self):      return self.options.get('status')
    def company(self):     return self.options.get('company')
    def subcompany(self):  return self.options.get('subcompany')
    def title(self):       return self.options.get('title')

    def image_left(self): return self.include_image('image_left')

    def image_right(self): return self.include_image('image_right')

    img_template = "\includegraphics[width=11mm, height=11mm]{%s}}"

    def include_image(self, name):
        result = self.options.get('image_right')
        if result is None: return ""
        return img_template % name.unix_style

###############################################################################
class FooterTemplate(Template):
    """All the parameters to be rendered in the LaTeX footer template"""
    pass