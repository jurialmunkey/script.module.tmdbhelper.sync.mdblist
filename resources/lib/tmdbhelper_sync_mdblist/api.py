from jurialmunkey.ftools import cached_property
from tmdbhelper.lib.api.request import RequestAPI
from tmdbhelper_sync_mdblist.settings import MDbListSettings
from tmdbhelper_sync_mdblist.ratings_mapping import (
    MDbListRatingMapping,
    MDbListSeasonRatingMapping,
    MDbListEpisodeRatingMapping,
)


class MDbList(RequestAPI):
    def __init__(self, api_key):
        super().__init__(
            req_api_key=f'apikey={api_key}',
            req_api_name='MDbList',
            req_api_url='https://api.mdblist.com')

    def modify_static_list(
            self, list_id, media_type, media_id, media_provider='tmdb', action='add'):
        item = {f'{media_type}s': [{media_provider: media_id}]}
        path = self.get_request_url('lists', list_id, 'items', action)
        return self.get_api_request(path, postdata=item, method='json')

    def get_details(
            self, media_type, media_id, media_provider='tmdb',
            append_to_response='keyword,episode_ratings'):
        return self.get_request_sc(
            media_provider, media_type, media_id, append_to_response=append_to_response)

    def get_ratings(self, media_type, media_id, media_provider='tmdb'):
        response = self.get_details(media_type, media_id, media_provider=media_provider)
        response = MDbListRatingMapping(response)
        return response.ratings

    def get_season_ratings(self, media_type, media_id, season=None, media_provider='tmdb'):
        response = self.get_details(media_type, media_id, media_provider=media_provider)
        response = MDbListSeasonRatingMapping(response)
        response.season = season
        return response.ratings

    def get_episode_ratings(self, media_type, media_id, season=None, episode=None, media_provider='tmdb'):
        response = self.get_details(media_type, media_id, media_provider=media_provider)
        response = MDbListEpisodeRatingMapping(response)
        response.season = season
        response.episode = episode
        return response.ratings

    def get_response(self, *args, **kwargs):
        return self.get_api_request(self.get_request_url(*args, **kwargs), headers=self.headers)

    def get_response_json(self, *args, **kwargs):
        try:
            return self.get_response(*args, **kwargs).json()
        except ValueError:
            return {}
        except AttributeError:
            return {}


def MDbListAPI():
    api_key = MDbListSettings().api_key
    return MDbList(api_key) if api_key else None


class MDbListContainerAPIs:
    @cached_property
    def mdblist_api(self):
        return self.get_mdblist_api()

    def get_mdblist_api(self):
        return MDbListAPI()
