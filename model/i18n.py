from pathlib import Path
from aiogram.contrib.middlewares.i18n import I18nMiddleware



I18N_DOMAIN = 'mybot'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'

"""
todo: release i18n in v3.0
"""

# Setup i18n middleware

i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)

lazy_gettext = i18n.lazy_gettext



