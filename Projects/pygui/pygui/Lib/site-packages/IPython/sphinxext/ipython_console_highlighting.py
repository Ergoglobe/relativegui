"""
reST directive for syntax-highlighting ipython interactive sessions.

"""

from sphinx import highlighting
from IPython.lib.lexers import IPyLexer

def setup(app):
    """Setup as a sphinx extension."""

    return {'parallel_read_safe': True, 'parallel_write_safe': True}

# Register the extension as a valid pygments lexer.
# Alternatively, we could register the lexer with pygments instead. This would
# require using setuptools entrypoints: http://pygments.org/docs/plugins

ipy2 = IPyLexer(python3=False)
ipy3 = IPyLexer(python3=True)

highlighting.lexers['ipython'] = ipy2
highlighting.lexers['ipython2'] = ipy2
highlighting.lexers['ipython3'] = ipy3
