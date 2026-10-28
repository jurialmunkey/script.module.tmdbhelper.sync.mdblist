from jurialmunkey.ftools import cached_property
from tmdbhelper.lib.items.directories.mapper_basic import ItemMapper


class MDbListDirectoryItemMapper(ItemMapper):
    type_art = False

    @cached_property
    def builder(self):
        return self.get_builder()

    def get_builder(self):
        return self.meta.item.item_builder(
            self.meta.item, self.meta.type, mixed_dir=True, type_art=self.type_art)

    @cached_property
    def label(self):
        return self.builder.label

    def get_params(self):
        return self.builder.params

    def get_art(self):
        return self.builder.art

    def get_infoproperties(self):
        return self.builder.infoproperties.copy()

    def get_context_menu(self):
        return self.builder.context_menu
