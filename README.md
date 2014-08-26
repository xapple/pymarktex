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