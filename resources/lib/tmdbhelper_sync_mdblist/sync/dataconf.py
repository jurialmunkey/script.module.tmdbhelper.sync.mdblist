from jurialmunkey.ftools import cached_property

"""
Convert MDBLIST sync data from episode based list into nested show list
To mimic Trakt data output for full,extended in sync/watched

EXAMPLE INPUT
{
    "last_watched_at": "2026-09-01T11:33:57.000Z",
    "episode": {
        "season": 1,
        "number": 10,
        "name": "The Verdict",
        "still": "https://image.tmdb.org/t/p/w200/5pnE91mUlCvr9PcAGo4e9IFs1cY.jpg",
        "ids": {
            "tmdb": 1178488,
            "tvdb": 5545827
        },
        "show": {
            "title": "American Crime Story",
            "year": 2016,
            "ids": {
                "tmdb": 64513,
                "trakt": 93939,
                "imdb": "tt2788432",
                "mdblist": "5cco"
            }
        }
    }
}

EXAMPLE OUTPUT
{
    "last_watched_at": "2026-09-01T11:33:57.000Z",
    "show": {
        "type": "show",
        "title": "American Crime Story",
        "year": 2016,
        "ids": {
            "tmdb": 64513,
            "trakt": 93939,
            "imdb": "tt2788432",
            "mdblist": "5cco"
        }
    }
    "seasons": [
        {
            "number": 1,
            "episodes": [
                {
                    "number": 10,
                    "last_watched_at": "2026-09-01T11:33:57.000Z",
                    "plays": 1,
                }
            ]
        }
    ]
}
"""


class ConfigureEpisodeDataItem:
    def __init__(self, item):
        self.item = item

    @cached_property
    def base(self):
        return self.item['episode']

    @cached_property
    def show(self):
        return dict(self.base['show'], type='show')

    @cached_property
    def tmdb(self):
        return self.show['ids'].get('tmdb')

    @cached_property
    def snum(self):
        return self.base['season']

    @cached_property
    def enum(self):
        return self.base['number']

    def get_episode(self):
        return {
            'number': self.enum, 'plays': 1,
            'last_watched_at': self.item['last_watched_at'],
        }


class ConfigureEpisodeData:
    def __init__(self):
        self.shows = {}

    def add_item(self, item):
        data = ConfigureEpisodeDataItem(item)
        show = self.shows.setdefault(data.tmdb, {'seasons': {}})
        show.update(show=data.show, last_watched_at=item['last_watched_at'])
        season = show['seasons'].setdefault(data.snum, {})
        season.setdefault(data.enum, data.get_episode())

    def get_finalised_show(self, show):
        return {
            'last_watched_at': show['last_watched_at'],
            'seasons': [
                {'number': number, 'episodes': list(episodes.values())}
                for number, episodes in show['seasons'].items()],
            'show': show['show'],
        }

    def get_items(self):
        return tuple(self.get_finalised_show(show) for show in self.shows.values())


def configure_episode_snapshot(episode_list, show_list):
    """ Restore the existing episode format with metadata fetched once per show. """
    try:
        shows = {
            item['show']['ids']['tmdb']: {k: item['show'][k] for k in ('title', 'year', 'ids')}
            for item in show_list
        }
        data = []
        for item in episode_list:
            if not item['show'] or not item['last_watched_at']:
                return
            if not isinstance(item['season'], int) or not isinstance(item['episode'], int):
                return
            data.append({
                'last_watched_at': item['last_watched_at'],
                'episode': {
                    'season': item['season'],
                    'number': item['episode'],
                    'show': shows[item['show']],
                },
            })
        return data
    except (AttributeError, KeyError, TypeError):
        return


def configure_episode_list(episode_list):
    data = ConfigureEpisodeData()
    for item in episode_list:
        data.add_item(item)
    return data.get_items()
