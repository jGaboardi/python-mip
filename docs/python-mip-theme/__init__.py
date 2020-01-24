import os
import re

from sphinx.util.compat import Directive


HTML_THEME_PATH = [os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '..'))]


# Storage for SEO descriptions.
seo_descriptions = {}

class SeoDescription(Directive):
    """
    This directive merely saves it's contents to the seo_descriptions dict
    under the document name key.
    """

    # this enables content in the directive
    has_content = True

    def run(self):
        # Save the last SEO description for a page.
        seo_descriptions[self.state.document.settings.env.docname] = ' '.join(self.content)
        # Must return a list of nodes.
        return []


def tt2nav(toctree, klass=None, appendix=None, divider=False):
    """
    Injects ``has-dropdown`` and ``dropdown`` classes to HTML
    generated by the :func:`toctree` function.
    
    :param str toctree:
        HTML generated by the :func:`toctree` function.
    """
    
    tt = toctree
    divider = '<li class="divider"></li>' if divider else ''
    
    # Append anything just before the closing </ul>.
    if appendix:
        tt = re.sub(r'(</ul>$)', r'{}\1'.format(appendix), tt)
    
    # Add class attribute to all <ul> elements.
    tt = re.sub(r'<ul>', r'<ul class="">', tt)
    
    # Add class to first <ul> tag.
    if klass:
        tt = re.sub(r'(^<ul[\s\w-]+class=")', r'\1{} '.format(klass), tt)
    
    # Add class "active" to all <li> tags with "current" class.
#    tt = re.sub(r'(<li[\s\w-]+class="[^"]*current)([^"]*")', r'\1 active\2', tt)
    
    # Match each <li> that contains <ul>.
    pattern = r'(<li[\s\w-]+class=")([^>]*>[^<]*<a[^>]*>[^<]*</a>[^<]*<ul[\s\w]+class=")'
    
    # Inject the classes.
    replace = r'{}\1has-dropdown \2dropdown '.format(divider)
    
    # Do the replace and return.
    return re.sub(pattern, replace, tt)


def hpc(app, pagename, templatename, context, doctree):
    # Add the tt2nav() callable to Jinja2 template context.
    context['tt2nav'] = tt2nav
    context['seo_description'] = seo_descriptions.get(pagename, '')


def setup(app):
    # Add directives.
    app.add_directive('seo-description', SeoDescription)
    
    # Hook the events.
    app.connect('html-page-context', hpc)
    