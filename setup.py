import os
from setuptools import setup, find_packages

try:
  readme = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
except:
  readme = ''

template_dir = "src/qartez/templates/qartez"
templates = [os.path.join(template_dir, f) for f in os.listdir(template_dir)]

version = '0.7'

setup(
    name='django-qartez',
    version=version,
    description=("Additional XML sitemap functionality for Django"),
    long_description=readme,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
    ],
    keywords='xml sitemaps, images sitemaps, django, app, python',
    author='Artur Barseghyan',
    author_email='artur.barseghyan@gmail.com',
    license='GPL 2.0/LGPL 2.1',
    url='https://bitbucket.org/barseghyanartur/django-qartez',
    package_dir={'': 'src'},
    packages=find_packages(where='./src'),
    package_data={'qartez': templates},
    include_package_data=True,
    install_requires=[
        'six>=1.1.0',
        'django-nine>=0.1.7'
    ],
    tests_require=[
        'radar>=0.3',
    ]
)
