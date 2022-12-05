import os

from datetime import datetime
from fastapi import FastAPI, Request, Response, status, Depends
from pymongo import MongoClient
from app.json_ld_utilities import JsonLdResponse
from app.media_type import MediaType
from app.web_annotation_data_model import WebAnnotationDataModel

app = FastAPI(title="Annotations API")

@app.get("/{collection_id}/",
    response_class=JsonLdResponse,
    dependencies=[Depends(MediaType.application_ld_json)])
def get_annotations(collection_id: str, page: int = None):
    client = MongoClient('mongodb://' + os.getenv('DB_USER') + ':' + os.getenv('DB_PASSWORD') + '@' + os.getenv('DB_HOST') + ':' + os.getenv('DB_PORT') + '/')
    db = client[os.getenv('DB_NAME')]
    annotations_db_collection = db[collection_id]
    total_count = annotations_db_collection.count_documents({})

    if page is None:
        items = []
        cursor = annotations_db_collection.find(skip=0, limit=10)

        for annotation in cursor:
            items.append({
                "id": os.getenv('BASE_URL') + collection_id + '/' + str(annotation['_id']),
                "type": "Annotation",
                "body": annotation['body'],
                "target": annotation['target'],
            })

        response_model = {
                "@context": [
                    "http://www.w3.org/ns/anno.jsonld",
                    "http://www.w3.org/ns/ldp.jsonld"
                    ],
                "id": os.getenv('BASE_URL') + collection_id + '/',
                "type": ["BasicContainer", "AnnotationCollection"],
                "total": total_count,
                "first": {
                    "id": os.getenv('BASE_URL') + collection_id + '/?page=0',
                    "type": "AnnotationPage",
                }
                    }
        
        if total_count > 10:
            response_model['first']['next'] = os.getenv('BASE_URL') + collection_id + '/?page=1'

        response_model['first']['items'] = items
        response_model['last'] = os.getenv('BASE_URL') + collection_id + '/?page=' + str(int((total_count - 1) / 10))
    

    return response_model

@app.post("/{collection_id}/",
    status_code=status.HTTP_201_CREATED,
    response_class=JsonLdResponse,
    dependencies=[
        Depends(MediaType.application_ld_json),
        Depends(WebAnnotationDataModel.context_json_ld),
        Depends(WebAnnotationDataModel.type_annotation),])
async def post_annotation(collection_id: str, request: Request, response: Response):
    incoming_request = await request.json()
    incoming_request['created'] = datetime.utcnow().isoformat()
    client = MongoClient('mongodb://' + os.getenv('DB_USER') + ':' + os.getenv('DB_PASSWORD') + '@' + os.getenv('DB_HOST') + ':' + os.getenv('DB_PORT') + '/')
    db = client[os.getenv('DB_NAME')]
    annotations_db_collection = db[collection_id]
    annotations_db_collection.insert_one(incoming_request)

    id = incoming_request.pop('_id')
    incoming_request['id'] = os.getenv('BASE_URL') + collection_id + '/' + str(id)

    response.headers['Allow'] = 'PUT,GET,OPTIONS,HEAD,DELETE,PATCH'
    response.headers['Location'] = incoming_request['id']

    return incoming_request