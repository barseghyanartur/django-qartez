from django.shortcuts import render
from django.http import Http404

from foo.models import FooItem


def browse(request, template_name='foo/browse.html'):
    """Browse.

    In the template, we show all available FooItems.

    :param django.http.HttpRequest request:
    :param str template_name:
    :return django.http.HttpResponse:
    """
    queryset = FooItem._default_manager.all().order_by('-date_published')

    context = {'items': queryset}

    return render(request, template_name, context)


def detail(request, slug, template_name='foo/detail.html'):
    """Foo item detail.

    In the template, we show the title and the body of the FooItem and links
    to all its' all available translations.

    :param django.http.HttpRequest request:
    :param str slug: Foo item slug.
    :param str template_name:
    :return django.http.HttpResponse:
    """
    try:
        item = FooItem._default_manager.get(slug=slug)
    except Exception as e:
        raise Http404

    context = {'item': item}

    return render(request, template_name, context)


def welcome(request, template_name='foo/welcome.html'):
    """Welcome page.

    :param django.http.HttpRequest request:
    :param str template_name:
    :return django.http.HttpResponse:
    """
    context = {}
    return render(request, template_name, context)


def contact(request, template_name='foo/contact.html'):
    """Contact page.

    :param django.http.HttpRequest request:
    :param str template_name:
    :return django.http.HttpResponse:
    """
    context = {}
    return render(request, template_name, context)
