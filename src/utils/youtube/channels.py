from dateutil.parser import parse

from .interface import IAPIObject


class ChannelThumbnail:
    def __init__(self, default, medium, high, *args, **kwargs):
        self.default = default
        self.medium = medium
        self.high = high


class ChannelSnippet:
    def __init__(self, id, title, description, published_at, thumbnail, country):
        self.id = id
        self.title = title
        self.description = description
        self.published_at = published_at
        self.thumbnail = thumbnail
        self.country = country


class Channels(IAPIObject):
    def __init__(self, part, id):
        self.part = part
        self.id = id

    def get_url(self):
        return "https://www.googleapis.com/youtube/v3/channels"

    def get_parameters(self):
        return {"part": self.part, "id": self.id}

    def parse_item(self, item):
        snippet = item["snippet"]
        thumbnails = snippet["thumbnails"]
        res = ChannelSnippet(
            **{
                "id": item["id"],
                "title": snippet["title"],
                "description": snippet["description"],
                "published_at": parse(snippet["publishedAt"]).replace(tzinfo=None),
                "country": snippet["country"],
                "thumbnail": ChannelThumbnail(
                    **{
                        "default": thumbnails["default"]["url"],
                        "medium": thumbnails["medium"]["url"],
                        "high": thumbnails["high"]["url"],
                    }
                ),
            }
        )
        return res
