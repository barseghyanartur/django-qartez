from django.conf.urls import url

from foo import views

urlpatterns = [
    # Foo items listing URL
    url(r'^$', view=views.browse, name='foo.browse'),

    # Contact URL
    url(r'^contact/$', view=views.contact, name='foo.contact'),

    # Welcome URL
    url(r'^welcome/$', view=views.welcome, name='foo.welcome'),

    # Foo item detail URL
    url(
        r'^(?P<slug>[\w\-\_\.\,]+)/$',
        view=views.detail,
        name='foo.detail'
    ),
]
