from .youtube import YouTubeDataAPI


class YouTubeDataAPIInstance:
    @classmethod
    def init(cls, api_key):
        cls.api_instance = YouTubeDataAPI(api_key)

    @classmethod
    def get_instance(cls):
        return cls.api_instance
