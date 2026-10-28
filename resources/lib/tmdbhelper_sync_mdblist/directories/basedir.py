from tmdbhelper_sync_mdblist.directories.item import MDbListDirItem


class BaseDirItemMDbListTopLists(MDbListDirItem):
    priority = 100
    label_localized = 32421
    label_type = 'localize'
    params = {'info': 'mdblist_toplists'}
    icon_name = 'toplists'
    types = ('both', )


class BaseDirItemMDbListCuratedLists(BaseDirItemMDbListTopLists):
    priority = 102
    label_localized = 32543
    params = {'info': 'mdblist_curatedlists'}
    icon_name = 'curatedlists'


class BaseDirItemMDbListOfficialLists(BaseDirItemMDbListTopLists):
    priority = 104
    label_localized = 32544
    label_type = 'standard'
    params = {'info': 'mdblist_officiallists'}
    icon_name = 'officiallists'
    types = ('movie', 'tv', )


class BaseDirItemMDbListStreamingCharts(BaseDirItemMDbListTopLists):
    priority = 106
    label_localized = 32545
    label_type = 'standard'
    params = {'info': 'mdblist_streamingcharts'}
    icon_name = 'streamingcharts'
    types = ('movie', 'tv', )


class BaseDirItemMDbListLikedLists(BaseDirItemMDbListTopLists):
    priority = 108
    label_localized = 32210
    params = {'info': 'mdblist_likedlists'}
    icon_name = 'likedlists'


class BaseDirItemMDbListYourLists(BaseDirItemMDbListTopLists):
    priority = 110
    label_localized = 32211
    params = {'info': 'mdblist_yourlists'}
    icon_name = 'yourlists'


class BaseDirItemMDbListSearchLists(BaseDirItemMDbListTopLists):
    priority = 120
    label_localized = 32361
    params = {'info': 'mdblist_searchlists'}
    icon_name = 'searchlists'


def get_all_mdblist_class_instances():
    from tmdbhelper.lib.addon.module import get_all_module_class_objects_by_priority
    return [clobj() for clobj in get_all_module_class_objects_by_priority(__name__)]
