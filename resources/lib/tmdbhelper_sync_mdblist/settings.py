from xbmcaddon import Addon


class MDbListSettings:
    addon_id = 'script.module.tmdbhelper.sync.mdblist'

    def __init__(self):
        self.addon = Addon(self.addon_id)

    @property
    def api_key(self):
        return self.addon.getSetting('apikey')

    def migrate_settings(self):
        legacy_addon = Addon('plugin.video.themoviedb.helper')
        legacy_key = legacy_addon.getSetting('mdblist_apikey')
        if not legacy_key:
            return
        destination_key = self.api_key or legacy_key
        if not self.api_key:
            self.addon.setSetting('apikey', destination_key)
        if self.api_key != destination_key:
            raise RuntimeError('Unable to save migrated MDbList API key')
        legacy_addon.setSetting('mdblist_apikey', '')
        if legacy_addon.getSetting('mdblist_apikey'):
            raise RuntimeError('Unable to clear legacy MDbList API key')
