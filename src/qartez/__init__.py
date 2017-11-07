__title__ = 'django-qartez'
__version__ = '0.7'
__build__ = 0x000007
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'

from django.utils import version

if isinstance(version.get_version(), float) and version.get_version() < 1.9:
    from .sitemaps import *
