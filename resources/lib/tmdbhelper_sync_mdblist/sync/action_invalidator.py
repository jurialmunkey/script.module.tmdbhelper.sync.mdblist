from tmdbhelper.lib.sync.action_invalidator import SyncActionInvalidator


class MDbListWatchedActionInvalidator(SyncActionInvalidator):
    def __init__(self, syncdata, provider, dependencies, remove):
        super().__init__(syncdata, provider, dependencies)
        self.remove = remove

    def invalidate_sync_item(self, item):
        if self.remove or item.method != 'sync/watched':
            return super().invalidate_sync_item(item)
        # Additions support incremental history; deletions need a full snapshot.
        self.syncdata.window.get_property(
            f'syncdecorators.timerlock.sync_data.{item.item_type}.{item.cache_method}',
            clear_property=True)
