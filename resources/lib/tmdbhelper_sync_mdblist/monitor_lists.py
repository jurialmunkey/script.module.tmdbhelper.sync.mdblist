from jurialmunkey.ftools import cached_property
from tmdbhelper.lib.addon.plugin import get_localized
from tmdbhelper.lib.items.directories.mapper_basic import ItemMapper
from tmdbhelper.lib.sync.providers.monitor_lists import MonitorListsSupplier
from tmdbhelper_sync_mdblist.consts import MDBLIST_MAX_ITEMS_PER_PAGE
from tmdbhelper_sync_mdblist.sync.pagination import MDbListSyncPage
from xbmc import Monitor


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
        if not self.provider.is_authorized():
            return []
        return self.get_watchlists() + [
            self.get_mapped_item(dict(item, user_slug=self.user_slug)) for item in self.entries
        ]

    def get_watchlists(self):
        return [self.get_mapped_item({
            'id': f'watchlist/{item_type}',
            'name': f'{get_localized(32193)} {get_localized(label)}',
            'user_slug': self.user_slug,
        }) for item_type, label in (('movie', 20342), ('show', 20343))]

    def get_mapped_item(self, item, add_infoproperties=None):
        return self.item_mapper_class(item, add_infoproperties).item

    def get_list_items(self, list_slug):
        if not self.provider.is_authorized():
            return
        if list_slug in ('watchlist/movie', 'watchlist/show'):
            return self.get_watchlist_items(list_slug.split('/')[1])
        response = self.provider.api.get_response('lists', list_slug, 'items')
        if not response:
            return
        return self.get_configured_items(response.json())

    def get_watchlist_page(self, item_type, cursor=None):
        response = self.provider.api.get_response(
            'watchlist/items', mediatype=item_type, limit=MDBLIST_MAX_ITEMS_PER_PAGE, cursor=cursor)
        if response is None or response.status_code != 200:
            return
        return MDbListSyncPage(response, self.get_configured_items)

    def get_watchlist_items(self, item_type):
        monitor = Monitor()
        items = []
        cursors = set()
        cursor = None
        while not monitor.abortRequested():
            page = self.get_watchlist_page(item_type, cursor)
            if page is None:
                return
            items.extend(page.items)
            if not page.has_next_page:
                return items
            cursor = page.next_cursor
            if cursor in cursors:
                raise ValueError('MDbList watchlist pagination repeated a cursor')
            cursors.add(cursor)

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
