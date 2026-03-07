# backend/seed.py
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from app.db.session import SessionLocal
from app.models.room import Room, RoomStatus
from app.models.user import User, UserRole
from app.core.security import get_password_hash


def seed_database():
    db = SessionLocal()
    try:
        # 1. Semente de Administradores Supremos
        if db.query(User).count() == 0:
            print("👤 Criando contas dos Administradores Supremos...")
            super_admins = ["Roberto Leôncio", "Vinícius Leôncio", "Paulo Roberto"]
            hashed_pw = get_password_hash("renascentehoteladmin07032026")

            for admin_name in super_admins:
                admin = User(
                    name=admin_name,
                    hashed_password=hashed_pw,
                    role=UserRole.SUPER_ADMIN,
                )
                db.add(admin)
            db.commit()
            print("✅ 3 Administradores Supremos criados com sucesso.")

        # 2. Semente de Quartos
        if db.query(Room).count() == 0:
            print("🏨 Plantando as sementes de quartos do Renascente Hotel... 🌱")
            initial_rooms = [
                Room(
                    number="101",
                    capacity=2,
                    has_ac=True,
                    has_breakfast=True,
                    status=RoomStatus.FREE,
                ),
                Room(
                    number="102",
                    capacity=1,
                    has_ac=False,
                    has_breakfast=True,
                    status=RoomStatus.FREE,
                ),
                Room(
                    number="201",
                    capacity=4,
                    has_ac=True,
                    has_breakfast=True,
                    status=RoomStatus.FREE,
                ),
                Room(
                    number="301",
                    capacity=2,
                    has_ac=True,
                    has_breakfast=True,
                    status=RoomStatus.MAINTENANCE,
                ),
            ]
            db.add_all(initial_rooms)
            db.commit()
            print(f"✅ {len(initial_rooms)} quartos adicionados ao banco de dados. ☀️")
    except Exception as e:
        print(f"❌ Erro ao popular o banco: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
