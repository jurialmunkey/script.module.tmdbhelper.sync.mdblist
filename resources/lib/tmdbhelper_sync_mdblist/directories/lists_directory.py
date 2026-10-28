from jurialmunkey.ftools import cached_property
from tmdbhelper.lib.items.directories.base.lists_base import BaseDirList
from tmdbhelper.lib.items.directories.lists_default import ListDefault, ListProperties
from tmdbhelper_sync_mdblist.directories.basedir import get_all_mdblist_class_instances
from tmdbhelper_sync_mdblist.directories.mapper_directory import MDbListDirectoryItemMapper


class MDbListBaseDirList(BaseDirList):
    @property
    def basedir(self):
        return get_all_mdblist_class_instances()


class ListMDbListDirectoryProperties(ListProperties):
    plugin_name = 'MDbList'
    container_content = ''
    item_mapper_class = MDbListDirectoryItemMapper

    @cached_property
    def entries(self):
        return self.get_entries()

    def get_entries(self):
        return [
            entry for entry in MDbListBaseDirList().get_basedir()
            if not self.group or int(self.group) == entry.item.group
        ]

    @cached_property
    def type_art(self):
        return len({entry.type for entry in self.entries}) > 1

    @cached_property
    def items(self):
        return self.get_items()

    def get_items(self):
        return [self.get_mapped_item(entry) for entry in self.entries]

    def get_mapped_item(self, item, add_infoproperties=None):
        mapper = self.item_mapper_class(item, add_infoproperties)
        mapper.type_art = self.type_art
        return mapper.item


class ListMDbListDirectory(ListDefault):
    list_properties_class = ListMDbListDirectoryProperties
    kodi_db = None

    def configure_list_properties(self, list_properties):
        list_properties = super().configure_list_properties(list_properties)
        list_properties.plugin_name = 'MDbList'
        list_properties.pagination = False
        return list_properties

    def get_items(self, group=None, **kwargs):
        self.list_properties.group = group
        return self.get_items_finalised()
