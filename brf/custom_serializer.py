import json
from typing import Any

from django.core.serializers.json import DjangoJSONEncoder


class BaseSerializer:
    def __init__(self, options):
        pass

    def dumps(self, value: Any) -> bytes:
        raise NotImplementedError

    def loads(self, value: bytes) -> Any:
        raise NotImplementedError


class JSONSerializer(BaseSerializer):
    encoder_class = DjangoJSONEncoder

    def dumps(self, value: Any) -> bytes:
        return json.dumps(str(value), cls=self.encoder_class).encode()

    def loads(self, value: bytes) -> Any:
        return json.loads(value.decode())
