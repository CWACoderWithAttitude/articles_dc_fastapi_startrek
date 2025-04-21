from fastapi import APIRouter, HTTPException, Request, status, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Any, Generator
from pydantic_settings import BaseSettings


def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session


class Settings(BaseSettings):
    db_url: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


DATABASE_URL = settings.db_url or "sqlite:///./startrek-ships.db"
# DATABASE_URL = "sqlite:///./startrek-ships.db"
# DATABASE_URL = "postgresql://star:trek@startrek_db/star-trek-db"
print(f"Using database URL: {DATABASE_URL}")
engine = create_engine(DATABASE_URL, echo=True)


class Ship(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    classification: str = Field(index=True)
    sign: str | None = Field(default=None, index=True)
    speed: str | None = Field(default=None, index=True)
    captain: str | None = Field(default=None, index=True)
    comment: str | None = Field(default=None, index=True)
    url: str | None = Field(default=None, index=False)


SQLModel.metadata.create_all(engine)

router = APIRouter(
    prefix="/ships", tags=["ships"]
)


@router.post("/", response_model=Ship, tags=["startrek", "ships"], status_code=status.HTTP_201_CREATED)
async def create_ship(ship: Ship, session: Session = Depends(get_session)):
    session.add(ship)
    session.commit()
    session.refresh(ship)
    return ship


@router.get("/", response_model=list[Ship], tags=["startrek", "ships"], status_code=status.HTTP_200_OK)
async def get_ships(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    ships = session.exec(select(Ship).offset(skip).limit(limit)).all()
    return ships


@router.put("/{ship_id}", response_model=Ship, tags=["startrek", "ships"], status_code=status.HTTP_200_OK)
async def update_ship(ship_id: int, ship: Ship, session: Session = Depends(get_session)):
    db_ship = session.get(Ship, ship_id)
    if not db_ship:
        return {"error": f"Ship {ship_id} not found"}
    for key, value in ship.model_dump(exclude_unset=True).items():
        setattr(db_ship, key, value)
    session.add(db_ship)
    session.commit()
    session.refresh(db_ship)
    return db_ship


@router.delete("/{ship_id}", tags=["startrek", "ships"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_ship(ship_id: int, session: Session = Depends(get_session)) -> None:
    db_ship = session.get(Ship, ship_id)
    if not db_ship:
        raise HTTPException(
            status_code=404, detail=f"Ship {ship_id} not found")
    session.delete(db_ship)
    session.commit()
    return None  # {"message": f"Ship #{ship_id} deleted successfully"}
