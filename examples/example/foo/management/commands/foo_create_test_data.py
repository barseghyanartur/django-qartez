from django.core.management.base import BaseCommand

import factories


NUM_ITEMS = 50


class Command(BaseCommand):

    def handle(self, *args, **options):
        factories.FooItemFactory.create_batch(NUM_ITEMS)
