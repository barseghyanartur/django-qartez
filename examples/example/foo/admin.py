from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from foo.models import FooItem


class FooItemAdmin(admin.ModelAdmin):
    """
    Foo item admin.
    """
    list_display = ('title', 'date_published')
    prepopulated_fields = {'slug': ('title',)}

    readonly_fields = ('date_created', 'date_updated',)

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'body', 'image', 'alternative_url')
        }),
        (_("Publication date"), {
            'classes': ('',),
            'fields': ('date_published',)
        }),
        (_("Additional"), {
            'classes': ('collapse',),
            'fields': ('date_created', 'date_updated') #,
        })
    )

    class Meta:
        app_label = _('Foo item')

admin.site.register(FooItem, FooItemAdmin)
