from jurialmunkey.ftools import cached_property
from tmdbhelper.lib.items.directories.lists_default import ListDefault, ListProperties
from tmdbhelper.lib.items.directories.mapper_basic import ItemMapper
from tmdbhelper.lib.addon.plugin import get_localized


def get_sort_methods_asc_desc(sort_by, localized_name):
    return [
        {
            'name': f'{localized_name}: {get_localized(584)}',
            'params': {'sort_by': sort_by, 'sort_how': 'asc'}
        },
        {
            'name': f'{localized_name}: {get_localized(585)}',
            'params': {'sort_by': sort_by, 'sort_how': 'desc'}
        },
    ]


def get_sort_methods(info=None):
    items = [
        {
            'name': f'{get_localized(32287)}: {get_localized(571)}',
            'params': {}
        },
    ]
    items += get_sort_methods_asc_desc('rank', get_localized(32286))
    items += get_sort_methods_asc_desc('score', get_localized(32072))
    items += get_sort_methods_asc_desc('usort', get_localized(32079))
    items += get_sort_methods_asc_desc('score_average', get_localized(563))
    items += get_sort_methods_asc_desc('released', get_localized(172))
    items += get_sort_methods_asc_desc('releasedigital', f'{get_localized(172)} ({get_localized(32245)})')
    items += get_sort_methods_asc_desc('imdbrating', f'IMDb {get_localized(563)}')
    items += get_sort_methods_asc_desc('imdbvotes', f'IMDb {get_localized(205)}')
    items += get_sort_methods_asc_desc('last_air_date', get_localized(32069))
    items += get_sort_methods_asc_desc('imdbpopular', f'IMDb {get_localized(32175)}')
    items += get_sort_methods_asc_desc('tmdbpopular', f'TMDb {get_localized(32175)}')
    items += get_sort_methods_asc_desc('rogerebert', 'Roger Ebert')
    items += get_sort_methods_asc_desc('rtomatoes', 'Rotten Tomatoes')
    items += get_sort_methods_asc_desc('rtaudience', 'Rotten Tomatoes Audience')
    items += get_sort_methods_asc_desc('metacritic', f'Metacritic {get_localized(563)}')
    items += get_sort_methods_asc_desc('myanimelist', f'MyAnimeList {get_localized(563)}')
    items += get_sort_methods_asc_desc('letterrating', f'Letterboxd {get_localized(563)}')
    items += get_sort_methods_asc_desc('lettervotes', f'Letterboxd {get_localized(205)}')
    items += get_sort_methods_asc_desc('budget', get_localized(32067))
    items += get_sort_methods_asc_desc('revenue', get_localized(32068))
    items += get_sort_methods_asc_desc('runtime', get_localized(180))
    items += get_sort_methods_asc_desc('title', get_localized(369))
    items += get_sort_methods_asc_desc('added', get_localized(32063))
    items += get_sort_methods_asc_desc('random', get_localized(590))

    return [
        i for i in items
        if (
            ('allowlist' not in i or info in i['allowlist'])
            and ('blocklist' not in i or info not in i['blocklist'])
        )]


class MDbListSortItemMapper(ItemMapper):
    @cached_property
    def label(self):
        return f'{self.meta["params"].get("list_name")} - {self.meta["method"]["name"]}'

    def get_params(self):
        params = self.meta['params'].copy()
        params.update(self.meta['method']['params'])
        return params


class ListMDbListSortProperties(ListProperties):
    container_content = ''
    item_mapper_class = MDbListSortItemMapper

    @cached_property
    def items(self):
        return self.get_items()

    def get_items(self):
        return [
            self.get_mapped_item({'method': method, 'params': self.params})
            for method in get_sort_methods(self.params['info'])
        ]

    def get_mapped_item(self, item, add_infoproperties=None):
        return self.item_mapper_class(item, add_infoproperties).item


class ListMDbListSortBy(ListDefault):
    list_properties_class = ListMDbListSortProperties
    kodi_db = None
    get_sort_methods = staticmethod(get_sort_methods)

    def configure_list_properties(self, list_properties):
        list_properties = super().configure_list_properties(list_properties)
        list_properties.plugin_name = ''
        list_properties.pagination = False
        return list_properties

    def get_items(self, info, parent_info=None, **kwargs):
        self.list_properties.params = dict(kwargs, info=parent_info)
        return self.get_items_finalised()
