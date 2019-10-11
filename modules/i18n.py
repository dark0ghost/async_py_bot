import logging
from pathlib import Path

from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from typing import Tuple, Any, Callable

from modules.Users import Users
from modules.modificators import override

I18N_DOMAIN = 'mybot'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'

"""
todo: release i18n in v3.0
"""

# Setup i18n middleware

log = logging.getLogger(__name__)


class ACLMiddleware(I18nMiddleware):
    def get_tg_lang(self, tg_user: types.User) -> str:
        lang = tg_user.language_code
        if lang:
            lang = lang.split('-')[0]
        else:
            lang = 'en'
        return lang

    @override()
    async def get_user_locale(self, action: str, args: Tuple[Any]):
        tg_user = types.User.get_current()
        *_, data = args
        if tg_user is None:
            data['locale'] = 'en'
            return 'en'
        is_new, user = await Users.get_user(tg_user)
        args[0].conf['is_new_user'] = is_new
        data['locale'] = user.lang
        data['user'] = user
        lang = user.lang or self.get_tg_lang(tg_user)
        return lang


i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)

lazy_gettext = i18n.lazy_gettext
