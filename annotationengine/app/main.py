import os

from datetime import datetime
from fastapi import FastAPI, Request, Response, status, Depends
from pymongo import MongoClient
from app.json_ld_utilities import JsonLdResponse
from app.media_type import MediaType
from app.web_annotation_data_model import WebAnnotationDataModel

app = FastAPI(title="Annotations API")

@app.get("/annotations/")
def get_annotations():
    return {"@context": [
        "http://www.w3.org/ns/anno.jsonld",
        "http://www.w3.org/ns/ldp.jsonld"
    ]}

@app.post("/annotations/",
    status_code=status.HTTP_201_CREATED,
    response_class=JsonLdResponse,
    dependencies=[
        Depends(MediaType.application_ld_json),
        Depends(WebAnnotationDataModel.context_json_ld),
        Depends(WebAnnotationDataModel.type_annotation),])
async def post_annotation(request: Request, response: Response):
    incoming_request = await request.json()
    incoming_request['created'] = datetime.utcnow().isoformat()
    client = MongoClient('mongodb://' + os.getenv('DB_USER') + ':' + os.getenv('DB_PASSWORD') + '@' + os.getenv('DB_HOST') + ':' + os.getenv('DB_PORT') + '/')
    db = client[os.getenv('DB_NAME')]
    annotations_db_collection = db['annotations']
    annotations_db_collection.insert_one(incoming_request)

    id = incoming_request.pop('_id')
    incoming_request['id'] = os.getenv('BASE_URL') + str(id)

    response.headers['Allow'] = 'PUT,GET,OPTIONS,HEAD,DELETE,PATCH'
    response.headers['Location'] = incoming_request['id']

    return incoming_request
