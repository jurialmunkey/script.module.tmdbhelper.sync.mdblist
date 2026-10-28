from tmdbhelper_sync_mdblist.actions.service import ItemAction
from tmdbhelper.lib.script.sync.provider import ItemSync as ProviderItemSync


class ItemSync(ProviderItemSync, ItemAction):
    pass
