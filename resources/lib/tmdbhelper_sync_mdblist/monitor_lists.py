from jurialmunkey.ftools import cached_property
from tmdbhelper.lib.items.directories.mapper_basic import ItemMapper
from tmdbhelper.lib.sync.providers.monitor_lists import MonitorListsSupplier


class MDbListMonitorListMapper(ItemMapper):
    @cached_property
    def label(self):
        return f'MDbList: {self.meta.get("name") or ""}'

    def get_params(self):
        return {
            'user_slug': self.meta['user_slug'],
            'list_slug': str(self.meta['id']),
        }


class MDbListMonitorLists(MonitorListsSupplier):
    item_mapper_class = MDbListMonitorListMapper

    @cached_property
    def entries(self):
        return self.get_entries()

    def get_entries(self):
        if not self.provider.is_authorized():
            return []
        return self.provider.api.get_response_json('lists/user') or []

    def get_lists(self):
        return [self.get_mapped_item(dict(item, user_slug=self.user_slug)) for item in self.entries]

    def get_mapped_item(self, item, add_infoproperties=None):
        return self.item_mapper_class(item, add_infoproperties).item

    def get_list_items(self, list_slug):
        if not self.provider.is_authorized():
            return
        response = self.provider.api.get_response('lists', list_slug, 'items')
        if not response:
            return
        return self.get_configured_items(response.json())

    def get_configured_items(self, data):
        entries = data.get('movies', []) + data.get('shows', [])
        return [item for item in (self.get_mapped_list_item(entry) for entry in entries) if item]

    @staticmethod
    def get_mapped_list_item(item):
        try:
            mediatype = item['mediatype']
            return {
                'type': mediatype,
                mediatype: {
                    'title': item['title'],
                    'ids': {
                        'tmdb': item['id'],
                        'imdb': item['imdb_id'],
                    },
                },
            }
        except (KeyError, TypeError):
            return
