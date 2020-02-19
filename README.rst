=============
django-qartez
=============
The missing XML sitemaps for Django.

.. image:: https://img.shields.io/pypi/v/django-qartez.svg
   :target: https://pypi.python.org/pypi/django-qartez
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/django-qartez.svg
    :target: https://pypi.python.org/pypi/django-qartez/
    :alt: Supported Python versions

.. image:: https://img.shields.io/travis/barseghyanartur/django-qartez/master.svg
   :target: http://travis-ci.org/barseghyanartur/django-qartez
   :alt: Build Status

.. image:: https://readthedocs.org/projects/django-qartez/badge/?version=latest
    :target: http://django-qartez.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/license-GPL--2.0--only%20OR%20LGPL--2.1--or--later-blue.svg
   :target: https://github.com/barseghyanartur/django-qartez/#License
   :alt: GPL-2.0-only OR LGPL-2.1-or-later

.. image:: https://coveralls.io/repos/github/barseghyanartur/django-qartez/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/barseghyanartur/django-qartez?branch=master
    :alt: Coverage

Features
========
At the moment the following XML sitemaps are implemented:

- `qartez.sitemaps.ImagesSitemap`: XML images sitemaps according to the `specs
  <http://www.google.com/support/webmasters/bin/answer.py?answer=178636>`__.

- `qartez.sitemaps.StaticSitemap`: Sitemap for service pages. Add named
  patterns or URLs to the sitemap to have it nicely displayed in a separate
  service XML sitemap.

- `qartez.sitemaps.RelAlternateHreflangSitemap`: Sitemaps: rel="alternate"
  hreflang="x" implementation. Read the `specs
  <http://support.google.com/webmasters/bin/answer.py?hl=en&answer=2620865>`__.

Prerequisites
=============
- Django: 1.11, 2.0, 2.1, 2.2 and 3.0.
- Python: 2.7, 3.5, 3.6, 3.7, 3.8

Installation
============
1. Install
----------
Latest stable version on PyPI:

.. code-block:: sh

    pip install django-qartez

Latest stable version from GitHub:

.. code-block:: sh

    pip install https://github.com/barseghyanartur/django-qartez/archive/stable.tar.gz

2. Add `qartez` to your `INSTALLED_APPS`
----------------------------------------

.. code-block:: python

    INSTALLED_APPS = (
        # ...
        'django.contrib.sitemaps',
        'qartez',
        # ...
    )

Usage and examples
==================
We have an imaginary foo app.

See the `example code
<https://github.com/barseghyanartur/django-qartez/tree/master/examples/example>`_.

foo/sitemap.py
--------------
.. code-block:: python

    from django.contrib.sitemaps import Sitemap

    from qartez.sitemaps import (
        ImagesSitemap, StaticSitemap, RelAlternateHreflangSitemap
    )

    from foo.models import FooItem

    # ---------------------- XML images sitemap part ---------------------------
    # Dictionary to feed to the images sitemap.
    foo_item_images_info_dict = {
        # Base queryset to iterate when procuding a site map
        'queryset': FooItem._default_manager.exclude(image=None),
        'image_location_field': 'image_url', # Image location (URL)
        'image_title_field': 'title', # Image title
        # An absolute URL of the page where image is shown
        'location_field': 'get_absolute_url'
    }

    # XML images sitemap.
    foo_item_images_sitemap = {
        'foo_item_images': ImagesSitemap(foo_item_images_info_dict,
                                         priority=0.6),
    }

    # ---------------------- Static sitemap part ---------------------------
    # Sitemap for service pages like welcome and feedback.
    foo_static_sitemap = StaticSitemap(priority=0.1, changefreq='never')
    foo_static_sitemap.add_named_pattern('foo.welcome')
    foo_static_sitemap.add_named_pattern('foo.contact')

    # ---------------------- Normal sitemap part ---------------------------
    # Normal Foo items sitemap.
    class FooItemSitemap(Sitemap):
        changefreq = "weekly"
        priority = 1.0

        def location(self, obj):
           return obj.get_absolute_url()

        def lastmod(self, obj):
           return obj.date_published

        def items(self):
           return FooItem._default_manager.all()

    # ---------------------- Alternate hreflang sitemap part ---------------
    # Alternate hreflang sitemap.
    class ArticleSitemap(RelAlternateHreflangSitemap):
        # If you want to serve the links on HTTPS.
        protocol = 'https'

        def alternate_hreflangs(self, obj):
           return [('en-us', obj.alternative_object_url),]

        def items(self):
           return FooItem._default_manager.all()

urls.py
-------
.. code-block:: python

    from foo.sitemap import foo_item_images_sitemap, foo_static_sitemap
    from foo.sitemap import FooItemAlternateHreflangSitemap, FooItemSitemap

    sitemaps = {
        'foo-items': FooItemSitemap,
        'foo-items-alternate-hreflang': FooItemAlternateHreflangSitemap,
        'foo-static': foo_static_sitemap
    }

    urlpatterns = [
        # Sitemaps
        (
            r'^sitemap\.xml$',
            'django.contrib.sitemaps.views.index',
            {'sitemaps': sitemaps},
        ),

        (
            r'^sitemap-foo-images\.xml$',
            'qartez.views.render_images_sitemap',
            {'sitemaps': foo_item_images_sitemap},
        ),
    ]

Note, that it's necessary to add the
```'template_name': 'qartez/rel_alternate_hreflang_sitemap.xml'```
only in case if you are going to use the ``qartez.RelAlternateHreflangSitemap``.

.. code-block:: python

    (
        r'^sitemap-(?P<section>.+)\.xml$',
        'django.contrib.sitemaps.views.sitemap',
        {
            'sitemaps': sitemaps,
            'template_name': 'qartez/rel_alternate_hreflang_sitemap.xml'
        }
    ),

In order to just get a better idea what kind of models and views are given in
the example, see the code parts below.

foo/models.py
-------------
.. code-block:: python

    class FooItem(models.Model):
        title = models.CharField(_("Title"), max_length=100)
        slug = models.SlugField(_("Slug"), unique=True)
        body = models.TextField(_("Body"))
        date_published = models.DateTimeField(
            _("Date published"),
            blank=True,
            null=True,
            auto_now_add=True
        )

        # Image to be used for XML images sitemap.
        image = models.ImageField(
            _("Headline image"),
            blank=True,
            null=True,
            upload_to='foo-images'
        )

        # URL to be used for alternative hreflang attribute.
        alternative_url = models.URLField(
            _("Alternative URL"),
            blank=True,
            null=True
        )

        class Meta:
           verbose_name = _("Foo item")
           verbose_name_plural = _("Foo items")

        def __str__(self):
           return self.title

        def get_absolute_url(self):
           kwargs = {'slug': self.slug}
           return reverse('foo.detail', kwargs=kwargs)

        # Shortcut to full image URL for XML images sitemap.
        def image_url(self):
           return self.image.url if self.image else ''

foo/views.py
------------
.. code-block:: python

    # Service welcome page
    def welcome(request, template_name='foo/welcome.html'):
        context = {}
        return render_to_response(
            template_name,
            context,
            context_instance=RequestContext(request)
        )

    # Service contact page
    def contact(request, template_name='foo/contact.html'):
        context = {}
        return render_to_response(template_name, context, \
                                  context_instance=RequestContext(request))

foo/urls.py
-----------
.. code-block:: python

    urlpatterns = patterns('foo.views',
        # ...
        # Contact URL
        url(r'^contact/$', view='contact', name='foo.contact'),
        # ...
        # Welcome URL
        url(r'^welcome/$', view='welcome', name='foo.welcome'),
        # ...
    )

License
=======
GPL-2.0-only OR LGPL-2.1-or-later

Support
=======
For any issues contact me at the e-mail given in the `Author`_ section.

Author
======
Artur Barseghyan <artur.barseghyan@gmail.com>
