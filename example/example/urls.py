from django.conf.urls import patterns, include, url

from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

from foo.sitemap import foo_item_images_sitemap, foo_static_sitemap, FooItemSitemap, FooItemAlternateHreflangSitemap, \
    FooImagesSitemap

sitemaps = {
    'foo-items': FooItemSitemap,
    'foo-items-alternate-hreflang': FooItemAlternateHreflangSitemap,
    'foo-static': foo_static_sitemap,
    'foo-images-custom': FooImagesSitemap,
}

admin.autodiscover()

urlpatterns = patterns('',
    # Foo URLs
    (r'^foo/', include('foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Sitemaps
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
    (r'^sitemap-foo-images\.xml$', 'qartez.views.render_images_sitemap', {'sitemaps': foo_item_images_sitemap}),

    # Note, that it's necessary to add the 'template_name': 'qartez/rel_alternate_hreflang_sitemap.xml' only in case
    # if you are going to use the ``qartez.RelAlternateHreflangSitemap``.
    (r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap',
     {'sitemaps': sitemaps, 'template_name': 'qartez/rel_alternate_hreflang_sitemap.xml'}),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
