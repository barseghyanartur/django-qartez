from django.conf import settings

from . import defaults

__title__ = 'qartez.conf'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('get_setting',)


def get_setting(setting, override=None):
    """
    Get a setting from ``qartez`` conf module, falling back to the default.

    If override is not None, it will be used instead of the setting.
    """
    if override is not None:
        return override
    if hasattr(settings, 'QARTEZ_{0}'.format(setting)):
        return getattr(settings, 'QARTEZ_{0}'.format(setting))
    else:
        return getattr(defaults, setting)
