Description
============================
Example Django project using `django-qartez`.

Installation
============================
Install requirements
----------------------------
    $ pip install -r ../requirements.txt

Create dataabse
----------------------------
    $ ./manage.py syncdb --noinput

Collect static files
----------------------------
    $ ./manage.py collectstatic --noinput

Run the server
----------------------------
    $ ./manage.py runserver

See the XML sitemaps
----------------------------
The following URLs should work in your browser (log in with admin:test):

Sitemap index:

    http://localhost:8000/sitemap.xml

Normal sitemap:

    http://localhost:8000/sitemap-foo-items.xml

Static sitemap:

    http://localhost:8000/sitemap-foo-static.xml


XML images sitemap:

    http://localhost:8000/sitemap-foo-images.xml

Alternate hreflang sitemap:

    http://localhost:8000/sitemap-foo-items-alternate-hreflang.xml
