from fastapi import APIRouter, HTTPException, Query
from app.models import LCARequest, LCAResponse, StatsResponse
from app.services import tree_service as svc

router = APIRouter(prefix="/api", tags=["persons"])


@router.get("/persons")
def list_persons():
    return svc.get_all_persons()


@router.get("/persons/{person_id}")
def get_person(person_id: str):
    person = svc.get_person(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@router.get("/generations")
def get_max_generation():
    return {"max_generation": svc.get_max_generation()}


@router.get("/generations/{n}")
def get_generation(n: int):
    return svc.get_by_generation(n)


@router.get("/search")
def search(q: str = Query(..., min_length=1)):
    return svc.search(q)


@router.get("/filter")
def filter_persons(type: str = Query("all")):
    return svc.filter_by_type(type)


@router.get("/stats", response_model=StatsResponse)
def get_stats():
    return svc.get_stats()


@router.get("/persons/{person_id}/path")
def get_path(person_id: str):
    if not svc.get_person(person_id):
        raise HTTPException(status_code=404, detail="Person not found")
    return {"path": svc.get_path_to_root(person_id)}


@router.post("/lca", response_model=LCAResponse)
def find_lca(body: LCARequest):
    lca_id, highlighted = svc.find_lca(body.ids)
    return LCAResponse(lca_id=lca_id, highlighted_ids=highlighted)
