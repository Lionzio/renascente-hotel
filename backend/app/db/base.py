# backend/app/db/base.py
from sqlalchemy.orm import declarative_base

# Apenas a declaração, sem importar os modelos de volta!
Base = declarative_base()
