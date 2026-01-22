from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi import FastAPI, Depends
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import Session

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/nfe101"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Loyer(Base):
    __tablename__ = "loyers"
    __table_args__ = {"schema": "projet2"}

    id = Column(Integer, primary_key=True)
    id_zone = Column(Integer)
    insee_c = Column(Integer)
    libgeo = Column(String(50))
    epci = Column(Text)
    dep = Column(Integer, index=True)
    reg = Column(Integer)
    loypredm2 = Column(String(50))
    lwr_ipm2 = Column(String(50))
    upr_ipm2 = Column(String(50))
    typpred = Column(String(50))
    nbobs_com = Column(Integer)
    nbobs_mail = Column(Integer)
    r2_adj = Column(String(50))

app = FastAPI(title="API TP nfe101")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def to_dict(obj):
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

@app.get("/loyers")
def get_all_loyers(db: Session = Depends(get_db)):
    rows = db.query(Loyer).all()
    return [to_dict(row) for row in rows]

@app.get("/loyers/{code_insee}")
def get_loyers_by_dep(code_insee: int, db: Session = Depends(get_db)):
    rows = db.query(Loyer).filter(Loyer.insee_c == code_insee).all()
    return [to_dict(row) for row in rows]