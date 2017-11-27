import datetime

from six import PY3
from six.moves.urllib import parse as urlparse

from django.contrib.sitemaps import Sitemap, GenericSitemap

from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured

from .constants import REL_ALTERNATE_HREFLANG_SITEMAP_TEMPLATE
from .settings import (
    PREPEND_LOC_URL_WITH_SITE_URL, PREPEND_IMAGE_LOC_URL_WITH_SITE_URL,
    CHANGEFREQ
)

from nine import versions

if versions.DJANGO_GTE_1_11:
    from django.urls import reverse_lazy
else:
    from django.core.urlresolvers import reverse_lazy

PY2 = not PY3

__title__ = 'django-qartez'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = (
    'ImagesSitemap',
    'StaticSitemap',
    'RelAlternateHreflangSitemap',
)


class ImagesSitemap(GenericSitemap):
    """Class for image sitemap.

    Implemented according to specs specified by Google
    http://www.google.com/support/webmasters/bin/answer.py?answer=178636

    :example:
    >>> from qartez.sitemaps import ImagesSitemap
    >>>
    >>> foo_item_images_info_dict = {
    >>>     'queryset': FooItem._default_manager.exclude(image=None), # qs
    >>>     'image_location_field': 'image', # image location
    >>>     'image_title_field': 'title', # image title
    >>>     'location_field': 'get_absolute_url' # an absolute URL of the page
    >>>                                          # where image is shown
    >>> }
    >>>
    >>> foo_item_images_sitemap = {
    >>>     'foo_item_images': ImagesSitemap(foo_item_images_info_dict, \
    >>>                                      priority=0.6),
    >>> }
    """

    def __init__(self, info_dict, priority=None, changefreq=None):
        """Constructor.

        :param dict info_dict:
        :param priority float:
        :param str changefreq:
        """
        self.image_location_field = info_dict.get('image_location_field', None)
        self.image_caption_field = info_dict.get('image_caption_field', None)
        self.image_title_field = info_dict.get('image_title_field', None)

        if self.image_title_field:
            if PY2:
                self.image_title_field = unicode(self.image_title_field)
            else:
                self.image_title_field = str(self.image_title_field)

        self.image_geo_location_field = info_dict.get(
            'image_geo_location_field', None
        )
        self.image_license_field = info_dict.get('image_license_field', None)
        self.location_field = info_dict.get('location_field', None)
        super(ImagesSitemap, self).__init__(info_dict, priority, changefreq)

    def image_location(self, item):
        """Get image location."""
        if self.image_location_field is not None:
            try:
                image_location_field = getattr(item, self.image_location_field)

                if callable(image_location_field):
                    return image_location_field()
                else:
                    return image_location_field
            except Exception as e:
                return None

        return None

    def image_caption(self, item):
        """Get image caption."""
        if self.image_caption_field is not None:
            return getattr(item, self.image_caption_field)
        return None

    def image_title(self, item):
        """Get image title."""
        if self.image_title_field is not None:
            return getattr(item, self.image_title_field)
        return None

    def image_geo_location(self, item):
        """Get image geo location."""
        if self.image_geo_location_field is not None:
            return getattr(item, self.image_geo_location_field)
        return None

    def image_license(self, item):
        """Get image geo location."""
        if self.image_license_field is not None:
            return getattr(item, self.image_license_field)
        return None

    def location(self, item):
        """
        Gets image location URL.
        """
        if self.location_field is not None:
            try:
                location_field = getattr(item, self.location_field)
                if callable(location_field):
                    return location_field()
                else:
                    return location_field
            except Exception as e:
                return None
        return item.get_absolute_url()

    def __get(self, name, obj, default=None):
        """Get method."""
        try:
            attr = getattr(self, name)
        except AttributeError:
            return default
        if callable(attr):
            return attr(obj)
        return attr

    def get_urls(self, page=1, site=None, protocol=None):
        """Get URLs."""
        # Determine protocol
        if self.protocol is not None:
            protocol = self.protocol
        if protocol is None:
            protocol = 'http'

        # Determine domain
        if site is None:
            if Site._meta.installed:
                try:
                    site = Site.objects.get_current()
                except Site.DoesNotExist:
                    pass
            if site is None:
                raise ImproperlyConfigured(
                    "To use sitemaps, either enable the sites framework or "
                    "pass a Site/RequestSite object in your view."
                )
        domain = site.domain

        urls = []
        for item in self.paginator.page(page).object_list:
            loc = self.__get('location', item, None)
            if loc and PREPEND_LOC_URL_WITH_SITE_URL:
                if PY2:
                    loc = "{0}://{1}{2}".format(
                        protocol, unicode(domain), unicode(loc)
                    )
                else:
                    loc = "{0}://{1}{2}".format(
                        protocol,
                        str(domain),
                        str(loc)
                    )

            image_loc = self.__get('image_location', item, None)
            if image_loc and PREPEND_IMAGE_LOC_URL_WITH_SITE_URL:
                try:
                    if PY2:
                        image_loc = "{0}://{1}{2}".format(
                            protocol, unicode(domain), unicode(image_loc)
                        )
                    else:
                        image_loc = "{0}://{1}{2}".format(
                            protocol, str(domain), str(image_loc)
                        )
                except Exception as e:
                    continue

            # Validating the changefreq
            changefreq = self.__get('changefreq', item, None)
            if changefreq is not None:
                assert changefreq in CHANGEFREQ

            # Validating the priority
            priority = self.__get('priority', item, None)
            if priority is not None:
                assert priority >= 0 and priority <= 1

            url_info = {
                'location': loc,
                'image_location': image_loc,
                'image_caption': self.__get('image_caption', item, None),
                'image_title': self.__get('image_title', item, None),
                'image_license': self.__get('image_license', item, None),
                'image_geo_location': self.__get(
                    'image_geo_location', item, None
                ),
                'lastmod': self.__get('lastmod', item, None),
                'changefreq': changefreq,
                'priority': priority
            }
            urls.append(url_info)
        return urls


class StaticSitemap(Sitemap):
    """Sitemap for ``static`` pages.

    See constructor docstring for list of accepted (additional) arguments.

    :example:
    >>> from qartez.sitemaps import StaticSitemap
    >>> service_sitemap = StaticSitemap(priority=0.1, changefreq='never')
    >>> service_sitemap.add_named_pattern('blog.welcome')
    >>> service_sitemap.add_named_pattern('feedback.contact')
    >>>
    >>> content_types_sitemap = StaticSitemap(priority=1.0, changefreq='daily')
    >>> content_types_sitemap.add_named_pattern('blog.browse') # Homepage
    >>> content_types_sitemap.add_named_pattern(
    >>>     'blog.browse', kwargs={'content_type': 'articles'}
    >>>     ) # Articles
    >>> content_types_sitemap.add_named_pattern(
    >>>     'blog.browse', kwargs={'content_type': 'downloads'}
    >>>     ) # Downloads
    """
    NAMED_PATTERN = 1
    URL = 2

    def __init__(self, *args, **kwargs):
        """Constructor. Accepts the following optional keyword-arguments (to
        be only specified as keyword-arguments).

        :param float priority:
        :param str changefreq:
        :param datetime.datetime|str lastmod:
        """
        if 'priority' in kwargs:
            self.priority = kwargs.pop('priority')
        else:
            self.priority = 1.0

        if 'changefreq' in kwargs:
            self.changefreq = kwargs.pop('changefreq')
        else:
            self.changefreq = 'never'

        if 'lastmod' in kwargs:
            self.lastmod = kwargs.pop('lastmod')
        else:
            self.lastmod = datetime.datetime.now()

        super(StaticSitemap, self).__init__(*args, **kwargs)
        self._items = []

    def items(self):
        """Return sitemap items.

        :return list:
        """
        return self._items

    def location(self, obj):
        """Location."""
        return obj['location']

    def add_named_pattern(self,
                          viewname,
                          urlconf=None,
                          args=[],
                          kwargs=None,
                          lastmod=None,
                          changefreq=None,
                          priority=None):
        """Ad a named pattern to the items list.

        :param str viewname:
        :param urlconf:
        :param list args:
        :param dict kwargs:
        :param lastmod:
        :param str changefreq:
        :param float priority:
        """
        try:
            loc = reverse_lazy(viewname, urlconf, args, kwargs)
            self._items.append({
                'location': loc,
                'lastmod': lastmod or self.lastmod,
                'changefreq': changefreq if changefreq else self.changefreq,
                'priority': priority if priority else self.priority
            })
        except Exception as e:
            pass

    def add_url(self, url, lastmod=None, changefreq=None, priority=None):
        """Add a URL to the items list.

        :param str url:
        :param lastmod:
        :param str changefreq:
        :param float priority:
        """
        try:
            self.items.append({
                'location': url,
                'lastmod': lastmod or self.lastmod,
                'changefreq': changefreq if changefreq else self.changefreq,
                'priority': priority if priority else self.priority
            })
        except Exception as e:
            pass

    def get_urls(self, *args, **kwargs):
        """Make sure nothing breaks if some URL is unresolvable.

        :return list:
        """
        try:
            return super(StaticSitemap, self).get_urls(*args, **kwargs)
        except Exception as e:
            return []


class RelAlternateHreflangSitemap(Sitemap):
    """Sitemaps: rel="alternate" hreflang="x" implementation.

    Read the specs the specs here
    http://support.google.com/webmasters/bin/answer.py?hl=en&answer=2620865

    IMPORTANT: When you use this class you have to override
    the ``alternate_hreflangs`` method in your sitemap class.

    :example:
    >>> from qartez.sitemaps import RelAlternateHreflangSitemap
    >>>
    >>> class ArticleSitemap(RelAlternateHreflangSitemap):
    >>>     def alternate_hreflangs(self, obj):
    >>>         return [('en-us', obj.alternative_object_url),]
    """

    def __get(self, name, obj, default=None):
        """Get."""
        try:
            attr = getattr(self, name)
        except AttributeError:
            return default
        if callable(attr):
            return attr(obj)
        return attr

    def alternate_hreflangs(self, item):
        """Alternate hreflangs.

        You should override the "alternate_hreflangs" method in your sitemap
        class.
        """
        raise NotImplementedError(
            """You have to override the "alternate_hreflangs" method in """
            """your sitemap class. Refer to "qartez" app documentation for """
            """details and examples."""
        )

    def _full_url(self, protocol, domain, path):
        """Full URL."""
        return "{0}://{1}{2}".format(protocol, domain, path)

    def _render_alternate_hreflangs(self, protocol, domain, item):
        """Render alternative hreflangs.

        Render the tiny bit of XML responsible for rendering the alternate
        hreflang code.

        :return str:
        """
        alternate_hreflangs = self.__get('alternate_hreflangs', item, [])
        output = ""
        if alternate_hreflangs:
            for lang, path in alternate_hreflangs:
                if urlparse.urlparse(path).netloc:
                    url = path
                else:
                    url = self._full_url(protocol, domain, path)
                output += REL_ALTERNATE_HREFLANG_SITEMAP_TEMPLATE.format(
                    **{'lang': lang, 'href': url}
                )
        return output

    def get_urls(self, page=1, site=None, protocol=None):
        """Get URLs."""
        # Determine protocol
        if self.protocol is not None:
            protocol = self.protocol
        if protocol is None:
            protocol = 'http'

        # Determine domain
        if site is None:
            if Site._meta.installed:
                try:
                    site = Site.objects.get_current()
                except Site.DoesNotExist:
                    pass
            if site is None:
                raise ImproperlyConfigured(
                    "To use sitemaps, either enable the sites framework "
                    "or pass a Site/RequestSite object in your view."
                )
        domain = site.domain

        urls = []
        for item in self.paginator.page(page).object_list:
            loc = self._full_url(
                protocol,
                domain,
                self.__get('location', item)
            )
            url_info = {
                'location': loc,
                'lastmod': self.__get('lastmod', item, None),
                'changefreq': self.__get('changefreq', item, None),
                'priority': self.__get('priority', item, None),
                'alternate_hreflangs': self._render_alternate_hreflangs(
                    protocol,
                    domain,
                    item
                ),
            }

            urls.append(url_info)
        return urls
