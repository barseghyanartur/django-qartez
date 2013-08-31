# Tiny bit of XML responsible for rendering the alternate hreflang code
REL_ALTERNATE_HREFLANG_SITEMAP_TEMPLATE = """
<xhtml:link
    rel="alternate"
    hreflang="%(lang)s"
    href="%(href)s"
    />
"""
