from xbmcaddon import Addon
from xbmcvfs import translatePath


ADDONPATH = translatePath(Addon('script.module.tmdbhelper.sync.mdblist').getAddonInfo('path'))

DIRECTORY_ICON_VARIANTS = {
    'curatedlists': ('both',),
    'likedlists': ('both',),
    'officiallists': ('movie', 'tv'),
    'searchlists': ('both',),
    'streamingcharts': ('movie', 'tv'),
    'toplists': ('both',),
    'yourlists': ('both',),
}


def get_icon(name, item_type=None):
    suffix = f'-{item_type}' if item_type in DIRECTORY_ICON_VARIANTS.get(name, ()) else ''
    return f'{ADDONPATH}/resources/icons/mdblist/{name}{suffix}.png'
