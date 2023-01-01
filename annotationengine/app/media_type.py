from fastapi import HTTPException, status, Header

class MediaType:
    @staticmethod
    def application_ld_json(content_type: str = Header(...)):
        """Require request MIME-type to be application/ld+json"""

        if content_type != 'application/ld+json; profile="http://www.w3.org/ns/anno.jsonld"':
            raise HTTPException(
                status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                "Content type must be 'application/ld+json; profile=\"http://www.w3.org/ns/anno.jsonld\"'.",
            )
