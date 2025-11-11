from fastapi import APIRouter

router = APIRouter(prefix="/assets", tags=["Assets"])

@router.get("/")
def get_assets():
    return {"message": "List of assets"}

@router.get("/{symbol}")
def get_asset(symbol: str):
    return {"message": f"Asset info for {symbol}"}
