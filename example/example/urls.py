from django.conf.urls import include, url

from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.contrib.sitemaps.views import index as sitemaps_index
from django.contrib.sitemaps.views import sitemap as sitemaps_sitemap
from qartez.views import render_images_sitemap

from foo.sitemap import (
    foo_item_images_sitemap, foo_static_sitemap, FooItemSitemap,
    FooItemAlternateHreflangSitemap, FooImagesSitemap
)

from foo import urls as foo_urls

sitemaps = {
    'foo-items': FooItemSitemap,
    'foo-items-alternate-hreflang': FooItemAlternateHreflangSitemap,
    'foo-static': foo_static_sitemap,
    'foo-images-custom': FooImagesSitemap,
}

admin.autodiscover()

urlpatterns = [
    # Foo URLs
    url(r'^foo/', include(foo_urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Sitemaps
    url(
        r'^sitemap\.xml$',
        sitemaps_index,
        {'sitemaps': sitemaps}
    ),
    url(
        r'^sitemap-foo-images\.xml$',
        render_images_sitemap,
        {'sitemaps': foo_item_images_sitemap}
    ),

    # Note, that it's necessary to add the
    # 'template_name': 'qartez/rel_alternate_hreflang_sitemap.xml' only in case
    # if you are going to use the ``qartez.RelAlternateHreflangSitemap``.
    url(
        r'^sitemap-(?P<section>.+)\.xml$',
        sitemaps_sitemap,
        {
            'sitemaps': sitemaps,
            'template_name': 'qartez/rel_alternate_hreflang_sitemap.xml'
        }
    ),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
