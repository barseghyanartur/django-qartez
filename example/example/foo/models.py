import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

FOO_IMAGES_STORAGE_PATH = 'foo-images'

def _foo_images(instance, filename):
    """
    Store the images in their own folder. This allows us to keep thumbnailed versions of all images.
    """
    if instance.pk:
        return '%s/%s-%s' % (FOO_IMAGES_STORAGE_PATH, str(instance.pk), filename.replace(' ', '-'))
    return '%s/%s' % (FOO_IMAGES_STORAGE_PATH, filename.replace(' ', '-'))


class FooItem(models.Model):
    """
    Foo item.
    """
    title = models.CharField(_("Title"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True)
    body = models.TextField(_("Body"))
    image = models.ImageField(_("Headline image"), blank=True, null=True, upload_to=_foo_images)
    alternative_url = models.URLField(_("Alternative URL"), blank=True, null=True)
    date_published = models.DateTimeField(_("Date published"), blank=True, null=True, default=datetime.datetime.now())
    date_created = models.DateTimeField(_("Date created"), blank=True, null=True, auto_now_add=True, editable=False)
    date_updated = models.DateTimeField(_("Date updated"), blank=True, null=True, auto_now=True, editable=False)

    class Meta:
        verbose_name = _("Foo item")
        verbose_name_plural = _("Foo items")

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        """
        Absolute URL, which goes to the foo item detail page.

        :return str:
        """
        kwargs = {'slug': self.slug}
        return reverse('foo.detail', kwargs=kwargs)

    @property
    def image_url(self):
        """
        Shortcut to full image URL for XML images sitemap.

        :return str:
        """
        return self.image.url if self.image else ''
