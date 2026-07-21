from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Import all models here
from app.models.user import User
from app.models.review import Review