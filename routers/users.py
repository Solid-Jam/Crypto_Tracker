from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def get_users():
    return {"message": "List of users"}

@router.post("/register")
def register_user():
    return {"message": "User registered successfully"}

@router.post("/login")
def login_user():
    return {"message": "User logged in successfully"}
