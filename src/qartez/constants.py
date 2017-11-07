__title__ = 'qartez.constants'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('REL_ALTERNATE_HREFLANG_SITEMAP_TEMPLATE',)

# Tiny bit of XML responsible for rendering the alternate hreflang code
REL_ALTERNATE_HREFLANG_SITEMAP_TEMPLATE = """
<xhtml:link rel="alternate" hreflang="{lang}" href="{href}"/>
"""
