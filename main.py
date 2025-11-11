from database import Base, engine
from models.models import User, Asset

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
