import sys
import os

# Adiciona o diretório atual ao path do Python para podermos importar o módulo 'app'
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.db.session import SessionLocal
from app.models.room import Room, RoomStatus


def seed_rooms():
    db = SessionLocal()
    try:
        # Verifica se já existem quartos para evitar duplicações se o script rodar duas vezes
        if db.query(Room).count() > 0:
            print("⚠️ O banco de dados já possui quartos cadastrados. Pulando o seed.")
            return

        print("Plantando as sementes do Renascente Hotel... 🌱")

        # Lista com a carga inicial de quartos do nosso hotel
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
                number="202",
                capacity=3,
                has_ac=True,
                has_breakfast=False,
                status=RoomStatus.FREE,
            ),
            Room(
                number="301",
                capacity=2,
                has_ac=True,
                has_breakfast=True,
                status=RoomStatus.MAINTENANCE,
            ),  # Um em manutenção para vermos a cor diferente no Frontend
        ]

        # Adiciona todos de uma vez e salva no banco
        db.add_all(initial_rooms)
        db.commit()

        print(
            f"✅ Sucesso! {len(initial_rooms)} quartos foram adicionados ao banco de dados. 🏨☀️"
        )

    except Exception as e:
        print(f"❌ Erro ao popular o banco: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_rooms()
