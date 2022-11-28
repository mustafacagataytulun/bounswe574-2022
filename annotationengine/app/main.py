from fastapi import FastAPI, Depends
from app.media_type import MediaType

app = FastAPI(title="Annotations API")

@app.get("/annotations/")
def get_annotations():
    return {"@context": [
        "http://www.w3.org/ns/anno.jsonld",
        "http://www.w3.org/ns/ldp.jsonld"
    ]}

@app.post("/annotations/", dependencies=[Depends(MediaType.application_ld_json)])
def post_annotation():
    return {}
