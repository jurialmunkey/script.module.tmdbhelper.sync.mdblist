from jurialmunkey.ftools import cached_property
from tmdbhelper.lib.addon.plugin import get_localized
from tmdbhelper.lib.script.method.kodi_utils import container_refresh
from xbmcgui import Dialog


class ItemLikeList:
    def __init__(self, provider, list_id, delete=False):
        self.provider = provider
        self.list_id = list_id
        self.delete = delete

    @property
    def mdblist_api(self):
        return self.provider.api

    @cached_property
    def response(self):
        return self.get_response()

    def get_response(self):
        return self.mdblist_api.like_list(self.list_id, delete=self.delete)

    @cached_property
    def is_successful(self):
        return self.get_is_successful()

    def get_is_successful(self):
        return self.response is not None and self.response.status_code == 200

    @property
    def dialog_header(self):
        return get_localized(32319 if self.delete else 32315)

    @cached_property
    def dialog_message(self):
        return self.get_dialog_message()

    def get_dialog_message(self):
        affix = get_localized(32320 if self.delete else 32321)
        message = get_localized(32316 if self.is_successful else 32317).format(affix)
        if not self.is_successful and self.response is not None:
            message = f'{message}\n{get_localized(32318).format(self.response.status_code)}'
        return message

    def sync(self):
        if self.mdblist_api is None:
            Dialog().ok(get_localized(32315), f'{get_localized(32516)}\n{get_localized(32517)}')
            return
        Dialog().ok(self.dialog_header, self.dialog_message)
        if self.is_successful:
            container_refresh()
