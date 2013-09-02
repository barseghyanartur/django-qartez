__title__ = 'qartez'
__version__ = '0.4'
__build__ = 0x000004
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('get_setting',)

from django.conf import settings

from qartez import defaults

def get_setting(setting, override=None):
    """
    Get a setting from ``qartez`` conf module, falling back to the default.

    If override is not None, it will be used instead of the setting.
    """
    if override is not None:
        return override
    if hasattr(settings, 'QARTEZ_%s' % setting):
        return getattr(settings, 'QARTEZ_%s' % setting)
    else:
        return getattr(defaults, setting)
