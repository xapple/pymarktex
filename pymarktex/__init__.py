b"""This module needs Python 2.7.x"""

# Special variables #
__version__ = '1.0.4'

# Built-in modules #
import os, sys, re, tempfile, shutil, codecs

# First party modules #
from plumbing.common import tail

# Third party modules #
import sh, pystache

# Get paths to module #
self = sys.modules[__name__]
module_dir = os.path.dirname(self.__file__)
repos_dir = os.path.abspath(module_dir + '/../') + '/'

# Various paths #
logo_dir = repos_dir + 'logos/'

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
            'image_path':  logo_dir + 'logo.png',
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
        # Header and Footer #
        from pymarktex.templates.sinclair_bio import HeaderTemplate, FooterTemplate
        self.header = HeaderTemplate(options) if header is None else header
        self.footer = FooterTemplate()        if footer is None else footer
        self.latex = str(self.header) + self.body + str(self.footer)

    def make_pdf(self, safe=False, include_src=False):
        """Call XeLaTeX (twice for cross-referencing)"""
        # Paths #
        self.tmp_dir    = tempfile.mkdtemp() + "/"
        self.tmp_path   = self.tmp_dir + 'main.tex'
        self.tmp_stdout = self.tmp_dir + 'stdout.txt'
        self.tmp_stderr = self.tmp_dir + 'stderr.txt'
        # Prepare #
        with codecs.open(self.tmp_path, 'w', encoding='utf8') as handle: handle.write(self.latex)
        self.params = ["--interaction=nonstopmode", '-output-directory']
        self.params += [self.tmp_dir, self.tmp_path]
        # Call twice for references #
        self.call_xelatex(safe)
        self.call_xelatex(safe)
        # Move into place #
        shutil.move(self.tmp_dir + 'main.pdf', self.output_path)
        # Show the latex source #
        if include_src: self.output_path.replace_extension('tex').write(self.latex, encoding='utf-8')

    def call_xelatex(self, safe=False):
        try:
            sh.xelatex(*self.params,
                        _ok_code=[0] if not safe else [0,1],
                        _err=self.tmp_stderr,
                        _out=self.tmp_stdout)
        except sh.ErrorReturnCode_1:
            print '-'*60
            print "Xelatex exited with return code 1."
            print "Here is the tail of the stdout at '%s':" % self.tmp_stdout
            print tail(self.tmp_stdout)
            print '-'*60
            raise

    def generate(self):
        self.load_markdown()
        self.make_body()
        self.make_latex(params=self.params)
        self.make_pdf()

    def web_export(self):
        """Copy the report to the webexport directory where it can be viewed by anyone"""
        self.web_location.directory.create(safe=True)
        shutil.copy(self.output_path, self.web_location)

    def purge_cache(self):
        """Some reports used pickled properties to avoid recalculations."""
        if not hasattr(self, 'cache_dir'): raise Exception("No cache directory to purge.")
        self.cache_dir.remove()

###############################################################################
class Template(object):
    """The template base class"""
    delimiters     = (u'@@[', u']@@')
    escape         = lambda s: lambda u: u # Needed otherwise celled with self
    str_encoding   = 'utf8'
    file_encoding  = 'utf8'

    def __repr__(self): return '<%s object on %s>' % (self.__class__.__name__, self.parent)
    def __str__(self): return self.render()

    def __init__(self, options=None):
        self.options = options if options else {}

    def render(self, escape=None, search_dirs=None, delimiters=None, str_encoding=None, file_encoding=None):
        delimiters    = self.delimiters    if delimiters is None    else delimiters
        pystache.defaults.DELIMITERS = delimiters
        escape        = self.escape        if escape is None        else escape
        #search_dirs   = self.search_dirs   if search_dirs is None   else search_dirs
        str_encoding  = self.str_encoding  if str_encoding is None  else str_encoding
        file_encoding = self.file_encoding if file_encoding is None else file_encoding
        renderer = pystache.Renderer(escape          = escape(),
                                     search_dirs     = search_dirs,
                                     string_encoding = str_encoding,
                                     file_encoding   = file_encoding)
        return renderer.render(self)