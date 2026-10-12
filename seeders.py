from sqlmodel import Session
from models import Disciplina
from database import engine

def seed_disciplinas():
    with Session(engine) as session:
        #so criar os bagulho
        Disciplina

if __name__ == "__main__":
    seed_disciplinas