import os
from setuptools import setup, find_packages

try:
  readme = open(os.path.join(os.path.dirname(__file__), 'readme.rst')).read()
except:
  readme = ''

template_dir = "src/qartez/templates/qartez"
templates = [os.path.join(template_dir, f) for f in os.listdir(template_dir)]

version = '0.4'

setup(
    name = 'django-qartez',
    version = version,
    description = ("Additional XML sitemap functionality for Django"),
    long_description = readme,
    classifiers = [
        "Framework :: Django",
        "Programming Language :: Python",
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords = 'xml sitemaps, images sitemaps, django, app, python',
    author = 'Artur Barseghyan',
    author_email = 'artur.barseghyan@gmail.com',
    license = 'GPL 2.0/LGPL 2.1',
    url = 'https://bitbucket.org/barseghyanartur/django-qartez',
    package_dir = {'':'src'},
    packages = find_packages(where='./src'),
    package_data = {'qartez': templates},
    include_package_data = True,
)
