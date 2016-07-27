"""
Settings module.

Override the following values in your global ``settings`` module by adding
`QARTEZ_` prefix to the values.

When it comes to importing the values, import them from ``qartez.settings``
module (without `QARTEZ_` prefix).

``PREPEND_LOC_URL_WITH_SITE_URL``: When set to True, current site's domain is
prepended to the location URL.

``PREPEND_IMAGE_LOC_URL_WITH_SITE_URL``: When set to True, current site's
domain is prepended to the image location URL.

``CHANGEFREQ``: Valid changefreq values according to the specs
http://www.sitemaps.org/protocol.html
"""

from .conf import get_setting

__title__ = 'qartez.settings'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = (
    'PREPEND_LOC_URL_WITH_SITE_URL', 'PREPEND_IMAGE_LOC_URL_WITH_SITE_URL',
    'CHANGEFREQ', 'DEBUG',
)

PREPEND_LOC_URL_WITH_SITE_URL = get_setting('PREPEND_LOC_URL_WITH_SITE_URL')
PREPEND_IMAGE_LOC_URL_WITH_SITE_URL = get_setting(
    'PREPEND_IMAGE_LOC_URL_WITH_SITE_URL'
    )
CHANGEFREQ = get_setting('CHANGEFREQ')

DEBUG = get_setting('DEBUG')
