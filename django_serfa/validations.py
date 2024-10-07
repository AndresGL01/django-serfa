import abc

from django.core.exceptions import ImproperlyConfigured
from schema import Schema, Optional

schema = Schema(
    {
        "services": [
            {
                "image": str,
                Optional("name"): str,
                "ports": [
                    {
                        "host": lambda x: isinstance(x, int) and (0 < x <= 65535),
                        "container": lambda x: isinstance(x, int) and (0 < x <= 65535)
                    }
                ],
                Optional("network"): str,
            }
        ],
    }
)


class BaseValidator(abc.ABC):
    @abc.abstractmethod
    def validate(self, value, settings):
        pass


class SerfaValidator(BaseValidator):
    def validate(self, value, settings) -> None:
        if not value:
            raise ImproperlyConfigured('SERFA_DEFINITION setting is missing. Please, add it on your settings.py file.')

        schema.validate(value)
