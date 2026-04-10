from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlmodel import Field, Session, SQLModel, create_engine, select

# ── Models ────────────────────────────────────────────────────────────────────

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
    power: Optional[str] = None

class HeroCreate(SQLModel):
    name: str
    secret_name: str
    age: Optional[int] = None
    power: Optional[str] = None

# ── Database ───────────────────────────────────────────────────────────────────

engine = create_engine("sqlite:///heroes.db", echo=True)

def create_db():
    SQLModel.metadata.create_all(engine)

# ── App ────────────────────────────────────────────────────────────────────────

app = FastAPI(title="Hero Registry API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db()

# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/heroes", response_model=List[Hero])
def get_heroes():
    with Session(engine) as session:
        return session.exec(select(Hero)).all()

@app.post("/heroes", response_model=Hero)
def create_hero(hero: HeroCreate):
    with Session(engine) as session:
        db_hero = Hero.from_orm(hero)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero

@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int):
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        session.delete(hero)
        session.commit()
        return {"ok": True}

# Serve the frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")
