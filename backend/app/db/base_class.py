# backend/app/db/base_class.py
import uuid
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID

# A Base do SQLAlchemy é criada APENAS AQUI para evitar importações circulares
Base = declarative_base()
