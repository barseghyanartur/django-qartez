django-qartez
======================================================
This app aims to provide the missing XML sitemapsf for Django. At the moment the following XML sitemaps are
implemented:

- qartez.ImagesSitemap: XML images sitemaps according to the specs
  http://www.google.com/support/webmasters/bin/answer.py?answer=178636

- qartez.StaticSitemap: Sitemap for service pages. Add named patterns or URLs to the sitemap to have it
  nicely displayed in a separate service XML sitemap.

- qartez.RelAlternateHreflangSitemap: Sitemaps: rel="alternate" hreflang="x" implementation. Read the specs
  the specs here http://support.google.com/webmasters/bin/answer.py?hl=en&answer=2620865

Prerequisites
======================================================
- Django 1.5.+
- Python 2.7.+, 3.3.+

Installation
======================================================
1. Install
------------------------------------------------------
Latest stable version on PyPI:

    $ pip install django-qartez

Latest stable version from bitbucket:

    $ pip install -e hg+http://bitbucket.org/barseghyanartur/django-qartez@stable#egg=django-qartez

Latest stable version from github:

    $ pip install -e git+https://github.com/barseghyanartur/django-qartez@stable#egg=django-qartez

2. Add `qartez` to your ``INSTALLED_APPS``
------------------------------------------------------
>>> INSTALLED_APPS = (
>>>     # ...
>>>     'django.contrib.sitemaps',
>>>     'qartez',
>>>     # ...
>>> )

Usage and examples
======================================================
We have an imaginary foo app.

The full source code of the example below is at http://bitbucket.org/barseghyanartur/django-qartez/src (see the
`example` directory).

foo/sitemap.py
------------------------------------------------------
>>> from django.contrib.sitemaps import Sitemap
>>>
>>> from qartez import ImagesSitemap, StaticSitemap, RelAlternateHreflangSitemap
>>>
>>> from foo.models import FooItem
>>>
>>> # ---------------------- XML images sitemap part ---------------------------
>>> # Dictionary to feed to the images sitemap.
>>> foo_item_images_info_dict = {
>>>     # Base queryset to iterate when procuding a site map
>>>     'queryset': FooItem._default_manager.exclude(image=None),
>>>     'image_location_field': 'image_url', # Image location (URL)
>>>     'image_title_field': 'title', # Image title
>>>     # An absolute URL of the page where image is shown
>>>     'location_field': 'get_absolute_url'
>>> }
>>>
>>> # XML images sitemap.
>>> foo_item_images_sitemap = {
>>>     'foo_item_images': ImagesSitemap(foo_item_images_info_dict, priority=0.6),
>>> }
>>>
>>> # ---------------------- Static sitemap part ---------------------------
>>> # Sitemap for service pages like welcome and feedback.
>>> foo_static_sitemap = StaticSitemap(priority=0.1, changefreq='never')
>>> foo_static_sitemap.add_named_pattern('foo.welcome')
>>> foo_static_sitemap.add_named_pattern('foo.contact')
>>>
>>> # ---------------------- Normal sitemap part ---------------------------
>>> # Normal Foo items sitemap.
>>> class FooItemSitemap(Sitemap):
>>>     changefreq = "weekly"
>>>     priority = 1.0
>>>
>>>     def location(self, obj):
>>>         return obj.get_absolute_url()
>>>
>>>     def lastmod(self, obj):
>>>         return obj.date_published
>>>
>>>     def items(self):
>>>         return FooItem._default_manager.all()
>>>
>>> # ---------------------- Alternate hreflang sitemap part ---------------
>>> # Alternate hreflang sitemap.
>>> class ArticleSitemap(RelAlternateHreflangSitemap):
>>>     # If you want to serve the links on HTTPS.
>>>     protocol = 'https'
>>>
>>>     def alternate_hreflangs(self, obj):
>>>         return [('en-us', obj.alternative_object_url),]
>>>
>>>     def items(self):
>>>         return FooItem._default_manager.all()

urls.py
------------------------------------------------------
>>> from foo.sitemap import foo_item_images_sitemap, foo_static_sitemap
>>> from foo.sitemap import FooItemAlternateHreflangSitemap, FooItemSitemap
>>>
>>> sitemaps = {
>>>     'foo-items': FooItemSitemap,
>>>     'foo-items-alternate-hreflang': FooItemAlternateHreflangSitemap,
>>>     'foo-static': foo_static_sitemap
>>> }
>>>
>>> urlpatterns = patterns('',
>>>     # Sitemaps
>>>     (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', \
>>>      {'sitemaps': sitemaps}),
>>>
>>>     (r'^sitemap-foo-images\.xml$', 'qartez.views.render_images_sitemap', \
>>>      {'sitemaps': foo_item_images_sitemap}),
>>> )

Note, that it's necessary to add the 'template_name': 'qartez/rel_alternate_hreflang_sitemap.xml'
only in case if you are going to use the ``qartez.RelAlternateHreflangSitemap``.

>>> (r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap',
>>>  {
>>>     'sitemaps': sitemaps,
>>>     'template_name': 'qartez/rel_alternate_hreflang_sitemap.xml'
>>>  }
>>> ),

In order to just get a better idea what kind of models and views are given in the example, see the code parts
below.

foo/models.py
------------------------------------------------------
>>> class FooItem(models.Model):
>>>     title = models.CharField(_("Title"), max_length=100)
>>>     slug = models.SlugField(_("Slug"), unique=True)
>>>     body = models.TextField(_("Body"))
>>>     date_published = models.DateTimeField(_("Date published"), blank=True, \
>>>                                           null=True, \
>>>                                           default=datetime.datetime.now())
>>>
>>>     # Image to be used for XML images sitemap.
>>>     image = models.ImageField(_("Headline image"), blank=True, null=True, \
>>>                               upload_to='foo-images')
>>>
>>>     # URL to be used for alternative hreflang attribute.
>>>     alternative_url = models.URLField(_("Alternative URL"), blank=True, null=True)
>>>
>>>     class Meta:
>>>         verbose_name = _("Foo item")
>>>         verbose_name_plural = _("Foo items")
>>>
>>>     def __unicode__(self):
>>>         return self.title
>>>
>>>     def get_absolute_url(self):
>>>         kwargs = {'slug': self.slug}
>>>         return reverse('foo.detail', kwargs=kwargs)
>>>
>>>     # Shortcut to full image URL for XML images sitemap.
>>>     def image_url(self):
>>>         return self.image.url if self.image else ''

foo/views.py
------------------------------------------------------
>>> # Service welcome page
>>> def welcome(request, template_name='foo/welcome.html'):
>>>     context = {}
>>>     return render_to_response(template_name, context, \
>>>                               context_instance=RequestContext(request))
>>>
>>> # Service contact page
>>> def contact(request, template_name='foo/contact.html'):
>>>     context = {}
>>>     return render_to_response(template_name, context, \
>>>                               context_instance=RequestContext(request))

foo/urls.py
------------------------------------------------------
>>> urlpatterns = patterns('foo.views',
>>>     # ...
>>>     # Contact URL
>>>     url(r'^contact/$', view='contact', name='foo.contact'),
>>>     # ...
>>>     # Welcome URL
>>>     url(r'^welcome/$', view='welcome', name='foo.welcome'),
>>>     # ...
>>> )

License
======================================================
GPL 2.0/LGPL 2.1

Support
======================================================
For any issues contact me at the e-mail given in the `Author` section.

Author
======================================================
Artur Barseghyan <artur.barseghyan@gmail.com>
