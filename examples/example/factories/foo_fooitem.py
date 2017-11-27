import os
import random

from django.conf import settings
from factory import DjangoModelFactory, SubFactory, LazyAttribute
from factory.fuzzy import FuzzyChoice

from foo.models import FooItem

from .factory_faker import Faker

__all__ = ('FooItemFactory',)


IMAGES = [
    os.path.join('foo-images', _path)
    for _path
    in os.listdir(os.path.join(settings.MEDIA_ROOT, 'foo-images'))
]


class BaseFooItemFactory(DjangoModelFactory):
    """Base FooItem factory."""

    title = Faker('text', max_nb_chars=100)
    slug = Faker('uuid4')
    body = Faker('text')
    image = FuzzyChoice(IMAGES)
    alternative_url = LazyAttribute(
        lambda __x: 'http://en-us.example.com/{}/'.format(
            random.randint(0, 100)
        )
    )
    date_published = Faker('date')
    date_created = Faker('date')
    date_updated = Faker('date')

    class Meta(object):
        """Meta class."""

        model = FooItem
        abstract = True


class FooItemFactory(BaseFooItemFactory):
    """Address factory."""
