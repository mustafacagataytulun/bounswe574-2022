import os

from datetime import datetime
from bson import ObjectId
from fastapi import FastAPI, Request, Response, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from app.json_ld_utilities import JsonLdResponse
from app.media_type import MediaType
from app.web_annotation_data_model import WebAnnotationDataModel

PER_PAGE: int = 10

app = FastAPI(title="Annotations API")

origins = [
    "https://colearnapp.mustafatulun.com",
    "http://localhost",
    "https://localhost",
    "http://localhost:8000",
    "https://localhost:8000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

@app.get("/{collection_id}/",
    response_class=JsonLdResponse,
    dependencies=[Depends(MediaType.application_ld_json)])
def get_annotations(collection_id: str, page: int = None, target: str = None, creator: str = None):
    client = MongoClient(os.getenv('DB_CONNECTION_STRING'))
    db = client[os.getenv('DB_NAME')]
    annotations_db_collection = db[collection_id]

    skip = 0

    if page is not None:
        skip = page * PER_PAGE

    query_filter = {}

    if target is not None and len(target) > 0:
        query_filter = {"$or":[{"target": target}, {"target.id": target}, {"target.source": target}]}

    if creator is not None and len(creator) > 0:
        query_filter = query_filter and {"$or":[{"creator": creator}, {"creator.id": creator}]}

    total_count = annotations_db_collection.count_documents(query_filter)
    items = []
    cursor = annotations_db_collection.find(query_filter, skip=skip, limit=PER_PAGE)

    for annotation in cursor:
        id = annotation.pop('_id')
        annotation.pop('@context')
        annotation['id'] = os.getenv('BASE_URL') + collection_id + '/' + str(id)
        items.append(annotation)

    if page is None:
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

        if total_count > PER_PAGE:
            response_model['first']['next'] = os.getenv('BASE_URL') + collection_id + '/?page=1'

        response_model['first']['items'] = items
        response_model['last'] = os.getenv('BASE_URL') + collection_id + '/?page=' + str(get_last_page_index(total_count))
    else:
        response_model = {
            "@context": "http://www.w3.org/ns/anno.jsonld",
            "id": os.getenv('BASE_URL') + collection_id + '/?page=' + str(page),
            "type": "AnnotationPage",
            "partOf": {
                "id": os.getenv('BASE_URL') + collection_id + '/',
                "total": total_count,
            },
            "startIndex": page * PER_PAGE,
            "items": items,
        }

        if page < get_last_page_index(total_count):
            response_model['next'] = os.getenv('BASE_URL') + collection_id + '/?page=' + str(page + 1)

        if page > 0:
            response_model['prev'] = os.getenv('BASE_URL') + collection_id + '/?page=0'

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
    client = MongoClient(os.getenv('DB_CONNECTION_STRING'))
    db = client[os.getenv('DB_NAME')]
    annotations_db_collection = db[collection_id]
    annotations_db_collection.insert_one(incoming_request)

    id = incoming_request.pop('_id')
    incoming_request['id'] = os.getenv('BASE_URL') + collection_id + '/' + str(id)

    response.headers['Allow'] = 'PUT,GET,OPTIONS,HEAD,DELETE,PATCH'
    response.headers['Location'] = incoming_request['id']

    return incoming_request

@app.delete("/{collection_id}/{annotation_id}",
    status_code=status.HTTP_204_NO_CONTENT)
async def delete_annotation(collection_id: str, annotation_id: str):
    client = MongoClient(os.getenv('DB_CONNECTION_STRING'))
    db = client[os.getenv('DB_NAME')]
    collection_list = db.list_collection_names()

    if collection_id not in collection_list:
        return JSONResponse({"message":"The collection does not exist."}, status_code=404)

    annotations_db_collection = db.get_collection(collection_id)

    deleted_annotation = annotations_db_collection.find_one_and_delete({'_id': ObjectId(annotation_id)})

    if deleted_annotation is None:
        return JSONResponse({"message":"The annotation does not exist."}, status_code=404)

def get_last_page_index(total_item_count: int):
    return int((total_item_count - 1) / PER_PAGE)
