from django.http import HttpResponse, Http404
from django.template import loader
from django.utils.encoding import smart_str
from django.core.paginator import EmptyPage, PageNotAnInteger

__title__ = 'qartez.views'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('render_images_sitemap',)


def render_images_sitemap(request, sitemaps, section=None,
                          template_name='qartez/images_sitemap.xml'):
    """Render images sitemap.

    :param django.http.HttpRequest request:
    :param sitemaps:
    :param secion:
    :param str template_name:
    :return django.http.HttpResponse:
    """
    maps, urls = [], []
    if section is not None:
        if section not in sitemaps:
            raise Http404(
                "No sitemap available for section: {0}".format(section)
                )
        maps.append(sitemaps[section])
    else:
        maps = sitemaps.values()
    page = request.GET.get("p", 1)
    for site in maps:
        try:
            if callable(site):
                urls.extend(site().get_urls(page))
            else:
                urls.extend(site.get_urls(page))
        except EmptyPage:
            raise Http404("Page {0} empty".format(page))
        except PageNotAnInteger:
            raise Http404("No page {0}".format(page))
    xml = smart_str(loader.render_to_string(
        template_name, {'urlset': urls, 'request': request})
        )
    try:
        return HttpResponse(xml, mimetype='application/xml')
    except TypeError:
        return HttpResponse(xml, content_type='application/xml')
