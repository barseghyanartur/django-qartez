__title__ = 'qartez.tests.test_sitemaps'
__author__ = 'Artur Barseghyan'
__copyright__ = 'Copyright (c) 2013-2014 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'

import unittest
import os

# Skipping from non-Django tests.
if os.environ.get("DJANGO_SETTINGS_MODULE", None):
    from django.test import Client

    from qartez.tests.base import print_info

    class QartezTest(unittest.TestCase):
        """
        Testing sitemaps.
        """
        def setUp(self):
            # Testing the URLs
            self.urls = {
                'sitemap of sitemaps': '/sitemap.xml',
                'normal sitemap': '/sitemap-foo-items.xml',
                'images sitemap': '/sitemap-foo-images.xml',
                'static sitemap': '/sitemap-foo-static.xml',
                'alternative hreflang sitemap': '/sitemap-foo-items-alternate-hreflang.xml',
            }

        @print_info
        def test_all_sitemaps(self):
            """
            Test the all sitemaps.
            """
            flow = []
            ## Testing view with signed URL
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
            """
            Test alternate hreflang sitemap.
            """
            flow = []
            c = Client()
            response = c.get('/sitemap-foo-items-alternate-hreflang.xml', {})
            self.assertTrue('hreflang="en-us"' in response.content)
            self.assertTrue('rel="alternate"' in response.content)
            self.assertTrue('hreflang="en-us"' in response.content)

        @print_info
        def test_02_static_sitemap(self):
            """
            Test static sitemap.
            """
            flow = []
            c = Client()
            response = c.get('/sitemap-foo-static.xml', {})
            self.assertTrue('http://example.com/foo/contact/' in response.content)

        @print_info
        def test_03_images_sitemap(self):
            """
            Test images sitemap.
            """
            flow = []
            c = Client()
            response = c.get('/sitemap-foo-images.xml', {})
            self.assertTrue('http://www.google.com/schemas/sitemap-image/1.1' in response.content)
            self.assertTrue('<image:title>' in response.content)
            self.assertTrue('<image:loc>' in response.content)
            self.assertTrue('<image:image>' in response.content)

        @print_info
        def test_04_sitemap_of_sitemaps(self):
            """
            Test sitemap of sitemaps.
            """
            flow = []
            c = Client()
            response = c.get('/sitemap.xml', {})
            self.assertTrue('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' in response.content)
            self.assertTrue('https://example.com/sitemap-foo-items-alternate-hreflang.xml' in response.content)
            self.assertTrue('http://example.com/sitemap-foo-items.xml' in response.content)


if __name__ == "__main__":
    # Tests
    unittest.main()
