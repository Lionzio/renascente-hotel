# backend/app/db/base.py
# 1. Importa a Base declarativa do base_class
from app.db.base_class import Base

# 2. Importa TODOS os modelos. O Alembic lê este ficheiro para criar as tabelas.
from app.models.user import User
from app.models.room import Room
from app.models.stay import Stay
from app.models.consumption import Consumption
from app.models.operations import Employee, CleaningRecord, MaintenanceRecord, RoomNote
