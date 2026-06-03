from fastapi import APIRouter
from pydantic import BaseModel
from bson import ObjectId
from backend.models import Asset # Import from the new models file

router = APIRouter(prefix="/assets", tags=["Assets"])

class AssetReq(BaseModel):
    asset_tag: str
    asset_type: str
    brand: str
    model: str
    serial_number: str
    department: str
    status: str
    notes: str

@router.post("/add")
def add_asset(req: AssetReq):
    Asset(**req.model_dump()).save() # Use model_dump() instead of dict() for newer Pydantic
    return {"message": "Asset added"}

@router.get("/all")
def get_all_assets():
    assets = []
    for a in Asset.objects():
        data = a.to_mongo().to_dict()
        data["id"] = str(data.pop("_id")) # Safely convert and remove ObjectId
        assets.append(data)
    return assets

@router.put("/{asset_id}")
def update_asset(asset_id: str, data: dict):
    asset = Asset.objects(id=ObjectId(asset_id)).first()
    if asset:
        asset.update(**data)
        return {"message": "Updated successfully"}
    return {"error": "Asset not found"}, 404

@router.delete("/{asset_id}")
def delete_asset(asset_id: str):
    Asset.objects(id=ObjectId(asset_id)).delete()
    return {"message": "Deleted successfully"}