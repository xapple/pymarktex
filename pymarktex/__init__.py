b"""This module needs Python 2.7.x"""

# Special variables #
__version__ = '1.0.4'

# Built-in modules #
import os, sys, re, tempfile, shutil, codecs

# Third party modules #
import sh, pystache

# Get paths to module #
self = sys.modules[__name__]
module_dir = os.path.dirname(self.__file__)
repos_dir = os.path.abspath(module_dir + '/../') + '/'

# Various paths #
logo_dir = repos_dir + 'logos/'

# Header and Footer #
from pymarktex.templates.envonautics import HeaderTemplate, FooterTemplate

###############################################################################
class Document(object):
    """The main object is the document to be generated from markdown text."""

    def __repr__(self): return '<%s object on %s>' % (self.__class__.__name__, self.parent)

    def __init__(self, input_path, output_path=None):
        # Input #
        self.input_path = input_path
        # Output #
        if output_path == None: self.output_path = self.default_output_name
        if output_path != None: self.output_path = output_path

    @property
    def default_options(self):
        return {
            'name':        os.environ.get('USER_FULL_NAME'),
            'status':      os.environ.get('USER_STATUS'),
            'company':     os.environ.get('USER_COMPANY'),
            'subcompany':  os.environ.get('USER_SUBCOMPANY'),
            'title':       "Auto-generated report",
            'image_left':  logo_dir + 'ebc.png',
            'image_right': logo_dir + 'uu.png',
            'image_path':  logo_dir + 'envonautics.png',
        }

    @property
    def default_output_name(self):
        return os.path.splitext(self.input_path)[0] + '.pdf'

    def load_markdown(self):
        """Load file in memory and separate the options and body"""
        if not os.path.exists(self.input_path): raise Exception("No file at %s." % self.input_path)
        with codecs.open(self.input_path, encoding='utf8') as handle: self.input = handle.read()
        self.params, self.markdown = re.findall('\A---(.+?)---(.+)', self.input, re.M|re.DOTALL)[0]
        # Parse the options #
        self.params = [i.partition(':')[::2] for i in self.params.strip().split('\n')]
        self.params = dict([(k.strip(),v.strip()) for k,v in self.params])

    def make_body(self):
        """Convert the body to LaTeX"""
        self.body = sh.pandoc(_in=self.markdown.encode('utf8'), read='markdown', write='latex')
        self.body = self.body.stdout.decode('utf8')

    def make_latex(self, params=None, header=None, footer=None):
        """Add the header and footer"""
        options = self.default_options.copy()
        if params: options.update(params)
        self.header = HeaderTemplate(options) if header is None else header
        self.footer = FooterTemplate()        if footer is None else footer
        self.latex = str(self.header) + self.body + str(self.footer)

    def make_pdf(self, safe=False):
        """Call XeLaTeX (twice for cross-referencing)"""
        self.tmp_dir  = tempfile.mkdtemp() + "/"
        self.tmp_path = self.tmp_dir + 'main.tex'
        with codecs.open(self.tmp_path, 'w', encoding='utf8') as handle: handle.write(self.latex)
        self.params = ["--interaction=nonstopmode", '-output-directory']
        self.params += [self.tmp_dir, self.tmp_path]
        sh.xelatex(*self.params, _ok_code=[0] if not safe else [0,1])
        sh.xelatex(*self.params, _ok_code=[0] if not safe else [0,1])
        # Move into place #
        shutil.move(self.tmp_dir + 'main.pdf', self.output_path)

    def generate(self):
        self.load_markdown()
        self.make_body()
        self.make_latex(params=self.params)
        self.make_pdf()

    def web_export(self):
        """Copy the report to the webexport directory where it can be viewed by anyone"""
        self.web_location.directory.create(safe=True)
        shutil.copy(self.output_path, self.web_location)

###############################################################################
class Template(object):
    """The template base class"""
    delimiters = (u'@@[', u']@@')
    escape     = lambda u: u
    str_encoding   = 'utf8'
    file_encoding  = 'utf8'

    def __repr__(self): return '<%s object on %s>' % (self.__class__.__name__, self.parent)
    def __str__(self): return self.render()

    def __init__(self, options=None):
        self.options = options if options else {}

    def render(self, escape=None, search_dirs=None, delimiters=None, str_encoding=None, file_encoding=None):
        escape        = self.escape        if escape is None        else escape
        search_dirs   = self.search_dirs   if search_dirs is None   else search_dirs
        delimiters    = self.delimiters    if delimiters is None    else delimiters
        str_encoding  = self.str_encoding  if str_encoding is None  else str_encoding
        file_encoding = self.file_encoding if file_encoding is None else file_encoding
        pystache.defaults.DELIMITERS = delimiters
        renderer = pystache.Renderer(escape          = escape,
                                     search_dirs     = search_dirs,
                                     string_encoding = str_encoding,
                                     file_encoding   = file_encoding)
        return renderer.render(self)