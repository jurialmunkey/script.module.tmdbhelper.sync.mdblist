from jurialmunkey.ftools import cached_property
from tmdbhelper.lib.items.directories.base.basedir_item import BaseDirItem
from tmdbhelper.lib.items.directories.base.item_builder import BaseDirItemBuilder
from tmdbhelper_sync_mdblist.directories.artwork import ADDONPATH, get_icon
from tmdbhelper_sync_mdblist.settings import MDbListSettings


class MDbListDirItemBuilder(BaseDirItemBuilder):
    def get_art(self):
        art = self.base_item.art.copy()
        if self.type_art:
            art['icon'] = get_icon(self.base_item.icon_name, self.item_type)
        return art


class MDbListDirItem(BaseDirItem):
    item_builder = MDbListDirItemBuilder
    icon_name = 'mdblist'

    @cached_property
    def art(self):
        return self.get_art()

    def get_art(self):
        return {
            'landscape': f'{ADDONPATH}/resources/fanart.jpg',
            'icon': get_icon(self.icon_name),
        }

    @property
    def enabled(self):
        return bool(MDbListSettings().api_key)


class MDbListDirectoryItem(MDbListDirItem):
    priority = 200
    label = 'MDbList'
    params = {'info': 'mdblist_directory'}
    types = (None,)
