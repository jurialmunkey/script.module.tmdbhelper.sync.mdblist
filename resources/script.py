from xbmc import executebuiltin
from jurialmunkey.parser import boolean


def run(like_list=None, delete=False):
    if like_list is None:
        executebuiltin(
            'RunScript(plugin.video.themoviedb.helper,configure_sync_provider,'
            'addon_id=script.module.tmdbhelper.sync.mdblist)')
        return
    import sys
    from os.path import join
    from xbmcaddon import Addon

    sys.path.insert(0, join(Addon('plugin.video.themoviedb.helper').getAddonInfo('path'), 'resources'))
    from tmdbhelper.lib.sync.providers.registry import SyncProviderRegistry
    provider = SyncProviderRegistry().find_provider('mdblist')
    if provider is None:
        return
    from tmdbhelper_sync_mdblist.actions.like import ItemLikeList
    ItemLikeList(provider, like_list, delete=boolean(delete)).sync()


if __name__ == '__main__':
    import sys
    run(**dict(arg.split('=', 1) for arg in sys.argv[1:]))
