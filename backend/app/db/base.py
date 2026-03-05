# backend/app/db/base.py
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Classe base do SQLAlchemy 2.0.
    Todos os modelos (Rooms, Users, etc.) devem herdar desta classe
    para que o metadata seja registrado corretamente no banco de dados.
    """

    pass
