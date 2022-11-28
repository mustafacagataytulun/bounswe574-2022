from typing import Any

import orjson
from fastapi import Response

class JsonLdResponse(Response):
    media_type = 'application/ld+json; profile="http://www.w3.org/ns/anno.jsonld"'

    def render(self, content: Any) -> bytes:
        return orjson.dumps(content)
