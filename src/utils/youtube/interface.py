import abc
from typing import Tuple


class IAPIObject(abc.ABC):
    def get_url(self) -> str:
        pass

    def get_http_method(self) -> str:
        pass

    def get_parameters(self) -> Tuple[str, dict]:
        pass

    def parse_item(self, item):
        pass
