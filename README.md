[![PyPI version](https://badge.fury.io/py/pymarktex.svg)](https://badge.fury.io/py/pymarktex)
[![changelog](http://allmychanges.com/p/python/pymarktex/badge/)](http://allmychanges.com/p/python/pymarktex/?utm_source=badge) 

# `pymarktex` version 1.2.4

This program creates a PDF file out of a specifically formated markdown text file.
In particular, the markdown file can contain extra information that
will be included in the final PDF with a fancy header. See the example included.

Dependencies:
* A text conversion engine. The `pandoc` executable should be in your `$PATH`.
* A latex engine. The `xelatex` executable should be in your `$PATH`.
* These two python libraries: `sh`, `pystache` (you can install them with `pip`).

You can use it from the shell like this:

    $ pymarktex lorem.md

And it will generate the corresponding `lorem.pdf` file in the same directory.

### Installing TeX Live

    $ wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
    $ tar xzf install-tl-unx.tar.gz
    $ cd install-tl-*
    $ ./install-tl -gui text

Then, change the install directory to something like: `~/programs/textlive/2014`

### Code documentation
More documentation is available at:
http://xapple.github.io/pymarktex/