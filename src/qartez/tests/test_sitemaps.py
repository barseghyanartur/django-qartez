from __future__ import unicode_literals

import os
import unittest

import pytest

__title__ = 'qartez.tests.test_sitemaps'
__author__ = 'Artur Barseghyan'
__copyright__ = '2013-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'


# Skipping from non-Django tests.
if os.environ.get("DJANGO_SETTINGS_MODULE", None):
    from django.test import Client
    from django.test import TestCase

    from qartez.tests.base import print_info

    import factories

    @pytest.mark.django_db
    class QartezTest(TestCase):
        """
        Testing sitemaps.
        """

        # fixtures = ['initial_data.json',]

        pytestmark = pytest.mark.django_db

        def setUp(self):
            # Testing the URLs
            self.urls = {
                'sitemap of sitemaps': '/sitemap.xml',
                'normal sitemap': '/sitemap-foo-items.xml',
                'images sitemap': '/sitemap-foo-images.xml',
                'static sitemap': '/sitemap-foo-static.xml',
                'alternative hreflang sitemap':
                    '/sitemap-foo-items-alternate-hreflang.xml',
                'images custom sitemap': '/sitemap-foo-images-custom.xml',
            }

            factories.FooItemFactory.create_batch(100)

        @print_info
        def test_all_sitemaps(self):
            """
            Test the all sitemaps.
            """
            flow = []
            # Testing view with signed URL
            client = Client()
            for description, url in self.urls.items():
                response = client.get(url, {})
                self.assertTrue(response.status_code in (200, 201, 202))
                flow.append(
                    'Response status code for {0} is {1}'.format(
                        description, response.status_code
                    )
                )

            return flow

        @print_info
        def test_01_alternative_hreflang_sitemap(self):
            """Test alternate hreflang sitemap."""
            flow = []
            c = Client()
            response = c.get('/sitemap-foo-items-alternate-hreflang.xml', {})
            response_content = response.content.decode()
            # import ipdb; ipdb.set_trace()
            self.assertTrue('hreflang="en-us"' in response_content)
            self.assertTrue('rel="alternate"' in response_content)
            # self.assertTrue(b'hreflang="en-us"' in response.content)

        @print_info
        def test_02_static_sitemap(self):
            """Test static sitemap."""
            flow = []
            c = Client()
            response = c.get('/sitemap-foo-static.xml', {})
            response_content = response.content.decode()
            self.assertTrue('http://example.com/foo/'
                            'contact/' in response_content)

        @print_info
        def test_03_images_sitemap(self):
            """Test images sitemap."""
            flow = []
            c = Client()
            response = c.get('/sitemap-foo-images.xml', {})
            response_content = response.content.decode()
            self.assertTrue('http://www.google.com/'
                            'schemas/sitemap-image/1.1' in response_content)
            self.assertTrue('<image:title>' in response_content)
            self.assertTrue('<image:loc>' in response_content)
            self.assertTrue('<image:image>' in response_content)

        @print_info
        def test_04_sitemap_of_sitemaps(self):
            """Test sitemap of sitemaps."""
            flow = []
            c = Client()
            response = c.get('/sitemap.xml', {})
            response_content = response.content.decode()
            self.assertTrue('<sitemapindex xmlns="'
                            'http://www.sitemaps.org/'
                            'schemas/sitemap/0.9">' in response_content)
            self.assertTrue('https://example.com/'
                            'sitemap-foo-items-alternate-'
                            'hreflang.xml' in response_content)
            self.assertTrue('http://example.com/sitemap-foo-'
                            'items.xml' in response_content)


if __name__ == "__main__":
    # Tests
    unittest.main()
