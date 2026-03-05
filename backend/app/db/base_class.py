# backend/app/db/base_class.py
from app.db.base import Base

# Importa todos os modelos para que o Alembic os detecte via target_metadata
from app.models.room import Room
from app.models.user import User
from app.models.stay import Stay
from app.models.consumption import Consumption
