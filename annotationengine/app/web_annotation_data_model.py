from fastapi import HTTPException, Request, status

class WebAnnotationDataModel:
    @staticmethod
    async def context_json_ld(request: Request):
        request_json = await request.json()
        context = request_json.get('@context')

        if ((isinstance(context, str) and context != 'http://www.w3.org/ns/anno.jsonld') or
            (not isinstance(context, str) and 'http://www.w3.org/ns/anno.jsonld' not in context)):
            raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    '@context must include "http://www.w3.org/ns/anno.jsonld".',
                )

    @staticmethod
    async def type_annotation(request: Request):
        request_json = await request.json()
        model_type = request_json.get('type')

        if ((isinstance(model_type, str) and model_type != 'Annotation') or
            (not isinstance(model_type, str) and 'Annotation' not in model_type)):
            raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    'type must include "Annotation".',
                )
