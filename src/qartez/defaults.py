__title__ = 'qartez'
__version__ = '0.4'
__build__ = 0x000004
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('PREPEND_LOC_URL_WITH_SITE_URL', 'PREPEND_IMAGE_LOC_URL_WITH_SITE_URL', 'CHANGEFREQ', 'DEBUG')

# When set to True, current site's domain is prepended to the location URL.
PREPEND_LOC_URL_WITH_SITE_URL = True

# When set to True, current site's domain is prepended to the image location URL.
PREPEND_IMAGE_LOC_URL_WITH_SITE_URL = True

# Valid changefreq values according to the specs http://www.sitemaps.org/protocol.html
CHANGEFREQ = ['always', 'hourly', 'daily', 'weekly', 'monthly', 'yearly', 'never']

DEBUG = False
