# Futures #
from __future__ import division

# Built-in modules #

# Internal modules #
from pymarktex import Template
from plumbing.autopaths import FilePath

# Third party modules #

###############################################################################
class LatexFigure(Template):
    def escape_underscore(self, text):
        if text is None: return None
        return text.replace('_', '\_')

###############################################################################
class ScaledFigure(LatexFigure):
    """A figure in latex code which can have its size adjusted"""

    def __repr__(self): return '<%s object on %s>' % (self.__class__.__name__, self.parent)

    def __init__(self, path, caption, label=None, **kwargs):
        # Attributes #
        self.path    = FilePath(path)
        self.caption = self.escape_underscore(caption)
        self.label   = self.escape_underscore(label)
        self.label   = r"\label{" + label + "}\n"    if label is not None else ''
        self.kwargs  = kwargs
        # Checks #
        if not self.path.exists: raise Exception("No file at '%s'." % self.path)
        if self.path.filename.count('.') > 1: raise Exception("Can't have several extension in a LaTeX figure file name.")

    def path(self): return self.path
    def caption(self): return self.caption
    def label(self): return self.label
    def graph_params(self):
        params = list('%s=%s' % (k,v) for k,v in self.kwargs.items())
        params += ['keepaspectratio']
        return ','.join(params)

###############################################################################
class DualFigure(LatexFigure):
    """A figure in latex code which has two subfigures"""

    def __repr__(self): return '<%s object on %s>' % (self.__class__.__name__, self.parent)

    def __init__(self, path_one, path_two, caption_one, caption_two, label_one, label_two, caption_main, label_main):
        # Attributes #
        self.path_one,    self.path_two    = FilePath(path_one), FilePath(path_two)
        self.caption_one, self.caption_two = map(self.escape_underscore, (caption_one, caption_two))
        self.label_one,   self.label_two   = map(self.escape_underscore, (label_one,   label_two))
        self.label_one    = r"\label{" + self.label_one + "}\n" if self.label_one is not None else ''
        self.label_two    = r"\label{" + self.label_two + "}\n" if self.label_two is not None else ''
        self.caption_main = self.escape_underscore(caption_main)
        self.label_main   = self.escape_underscore(label_main)
        self.label_main   = r"\label{" + self.label_main + "}\n" if self.label_main is not None else ''
        # Check #
        if not self.path_one.exists or not self.path_two.exists: raise Exception("File missing.")
        if self.path_one.filename.count('.') > 1 or self.path_two.filename.count('.') > 1:
            raise Exception("Can't have several extension in a LaTeX figure file name.")

    def path_one(self):     return self.path_one
    def path_two(self):     return self.path_two
    def caption_one(self):  return self.caption_one
    def caption_two(self):  return self.caption_two
    def label_one(self):    return self.label_one
    def label_two(self):    return self.label_two
    def caption_main(self): return self.caption_main