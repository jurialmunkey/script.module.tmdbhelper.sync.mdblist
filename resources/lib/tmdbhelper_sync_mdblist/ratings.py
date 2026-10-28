from jurialmunkey.ftools import cached_property
from tmdbhelper.lib.addon.plugin import convert_type
from tmdbhelper.lib.sync.providers.ratings import RatingsSupplier


class MDbListRatingsSupplier(RatingsSupplier):
    @cached_property
    def trakt_type(self):
        return convert_type(self.tmdb_type, 'trakt')

    def get_ratings(self):
        if not self.provider.is_authorized():
            return {}
        return self.get_api_ratings() or {}

    def get_api_ratings(self):
        return self.provider.api.get_ratings(self.trakt_type, self.tmdb_id)


class MDbListSeasonRatingsSupplier(MDbListRatingsSupplier):
    def get_api_ratings(self):
        return self.provider.api.get_season_ratings(self.trakt_type, self.tmdb_id, self.season)


class MDbListEpisodeRatingsSupplier(MDbListSeasonRatingsSupplier):
    def get_api_ratings(self):
        return self.provider.api.get_episode_ratings(
            self.trakt_type, self.tmdb_id, self.season, self.episode)
