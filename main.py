from fastapi import FastAPI
from routers import users, assets
from database import Base, engine
from models import models

app = FastAPI(title="Crypto Tracker API")

# Create all database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(users.router)
app.include_router(assets.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Crypto Tracker API"}
