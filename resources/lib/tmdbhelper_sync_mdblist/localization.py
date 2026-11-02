from xbmcaddon import Addon
from tmdbhelper.lib.addon.plugin import get_localized as get_core_localized


ADDON = Addon('script.module.tmdbhelper.sync.mdblist')
LOCALIZED_IDS = frozenset((
    32067, 32068, 32069, 32072, 32079, 32133, 32421,
    32516, 32517, 32518, 32543, 32544, 32545,
))


def get_localized(localize_int=0):
    if localize_int in LOCALIZED_IDS:
        return ADDON.getLocalizedString(localize_int)
    return get_core_localized(localize_int)
