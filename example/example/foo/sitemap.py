__all__ = ('foo_item_images_sitemap', 'foo_static_sitemap', 'FooItemSitemap')

from django.contrib.sitemaps import Sitemap

from qartez.sitemaps import ImagesSitemap, StaticSitemap, RelAlternateHreflangSitemap

from foo.models import FooItem

foo_item_images_info_dict = {
    'queryset': FooItem._default_manager.exclude(image=None), # Queryset
    'image_location_field': 'image_url', # Image location
    'image_title_field': 'title', # Image title
    'location_field': 'get_absolute_url' # An absolute URL of the page where image is shown
}

foo_item_images_sitemap = {
    'foo_item_images': ImagesSitemap(foo_item_images_info_dict, priority=0.6),
}

# Sitemap for service pages like welcome and feedback.
foo_static_sitemap = StaticSitemap(priority=0.1, changefreq='never')
foo_static_sitemap.add_named_pattern('foo.welcome')
foo_static_sitemap.add_named_pattern('foo.contact')

class FooItemSitemap(Sitemap):
    """
    Foo items sitemap.
    """
    changefreq = "weekly"
    priority = 1.0

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return obj.date_published

    def items(self):
        return FooItem._default_manager.all()

class FooItemAlternateHreflangSitemap(RelAlternateHreflangSitemap):
    """
    Alternative URL.
    """
    # If you want to serve the links on HTTPS.
    protocol = 'https'

    def alternate_hreflangs(self, item):
        return [('en-us', item.alternative_url),]

    def items(self):
        return FooItem._default_manager.exclude(alternative_url=None)

class FooImagesSitemap(ImagesSitemap):
    
    def __init__(self):
        super(FooImagesSitemap, self).__init__({
            'queryset': FooItem._default_manager.exclude(image=None), # queryset
            'image_location_field': 'image', # image location
            'image_title_field': 'title', # image title
            'location_field': 'get_absolute_url' # an absolute URL of the page
                                             # where image is shown    
        }, changefreq='weekly')
    

