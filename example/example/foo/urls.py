from django.conf.urls import patterns, url

urlpatterns = patterns('foo.views',
    # Foo items listing URL
    url(r'^$', view='browse', name='foo.browse'),

    # Contact URL
    url(r'^contact/$', view='contact', name='foo.contact'),

    # Welcome URL
    url(r'^welcome/$', view='welcome', name='foo.welcome'),

    # Foo item detail URL
    url(r'^(?P<slug>[\w\-\_\.\,]+)/$', view='detail', name='foo.detail'),
)
