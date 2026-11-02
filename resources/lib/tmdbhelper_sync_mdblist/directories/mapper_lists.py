from tmdbhelper_sync_mdblist.directories.artwork import get_icon
from tmdbhelper.lib.items.directories.mapper_standard import MediaItemMapper
from jurialmunkey.ftools import cached_property
from tmdbhelper.lib.addon.plugin import get_localized
from tmdbhelper.lib.addon.consts import RUNSCRIPT


class ListsMDbListItemMapper(MediaItemMapper):

    tmdb_type = ''
    mediatype = ''
    delete_like = False

    @cached_property
    def label(self):
        return self.meta.get('name') or ''

    infolabels_map = {
        'description': 'plot',
    }
    infoproperties_map = {
        'items': 'items',
        'likes': 'likes',
    }

    @property
    def icon(self):
        return get_icon('mdblist')

    def get_art(self):
        art = {'icon': self.icon}
        return art

    def get_infoproperties(self):
        infoproperties = super().get_infoproperties()
        infoproperties['is_sortable'] = 'mdblist'
        infoproperties['sortby_info'] = 'mdblist_sortby'
        return infoproperties

    def get_sort_context_menu(self):
        return [
            (
                get_localized(32309),
                RUNSCRIPT.format('sort_list,{}'.format(','.join(f'{k}={v}' for k, v in self.params.items())))
            ),
        ]

    def get_like_context_menu(self):
        command = f'like_list={self.meta["id"]}'
        command = f'{command},delete=true' if self.delete_like else command
        return [
            (
                get_localized(32319 if self.delete_like else 32315),
                f'RunScript(script.module.tmdbhelper.sync.mdblist,{command})'
            ),
        ]

    def get_context_menu(self):
        return self.get_sort_context_menu() + [
            (
                get_localized(20444),
                RUNSCRIPT.format(f'user_list={self.meta["id"]},user_slug=__api_mdblist__')
            ),
        ] + self.get_like_context_menu()

    def get_unique_ids(self):
        unique_ids = {
            'list_id': self.meta['id'],
            'user_id': self.meta.get('user_id'),
            'user_name': self.meta.get('user_name'),
            'list_slug': self.meta.get('slug'),
        }
        return unique_ids

    def get_params(self):
        params = {
            'info': 'mdblist_userlist',
            'list_id': self.meta['id'],
            'list_name': self.label,
            'plugin_category': self.label,
        }
        return params


class LikedListsMDbListItemMapper(ListsMDbListItemMapper):
    delete_like = True


class OfficialListsMDbListItemMapper(ListsMDbListItemMapper):

    def __init__(self, *args, tmdb_type, **kwargs):
        super().__init__(*args, **kwargs)
        self.tmdb_type = tmdb_type

    def get_context_menu(self):
        return self.get_sort_context_menu()

    def get_params(self):
        params = super().get_params()
        params['info'] = 'mdblist_officiallist'
        params['list_id'] = self.meta['slug']
        params['tmdb_type'] = self.tmdb_type
        return params
