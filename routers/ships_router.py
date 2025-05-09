from fastapi import APIRouter, HTTPException, Request, status, Depends
from sqlmodel import SQLModel, Session, create_engine, select
from typing import Any, Generator, Sequence

from settings import Settings
from ship_model import Ship


def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session


settings = Settings()


DATABASE_URL = settings.db_url or "sqlite:///./startrek-ships.db"
# DATABASE_URL = "sqlite:///./startrek-ships.db"
# DATABASE_URL = "postgresql://star:trek@startrek_db/star-trek-db"
print(f"Using database URL: {DATABASE_URL}")
engine = create_engine(DATABASE_URL, echo=True)


SQLModel.metadata.create_all(engine)

router = APIRouter(
    prefix="/ships", tags=["ships"]
)


@router.post("/", response_model=Ship, tags=["startrek", "ships"], status_code=status.HTTP_201_CREATED)
async def create_ship(ship: Ship, session: Session = Depends(get_session)) -> Ship:
    """
    Create a new ship.
    Args:
        ship (Ship): The ship object to create.
        session (Session): The database session.
    Returns:
        Ship: The created ship object.
    """
    session.add(ship)
    session.commit()
    session.refresh(ship)
    return ship


@router.get("/", response_model=list[Ship], tags=["ships"], status_code=status.HTTP_200_OK)
async def get_ships(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)) -> Sequence[Ship]:
    """
    Get a list of ships.

    Args:
        skip (int): The number of ships to skip.
        limit (int): The maximum number of ships to return.
        session (Session): The database session.
    Returns:
        list[Ship]: A list of ship objects. 
        """
    ships = session.exec(select(Ship).offset(skip).limit(limit)).all()
    return ships


@router.get("/{ship_id}", response_model=Ship, tags=["ships"], status_code=status.HTTP_200_OK)
async def get_ship_by_id(ship_id: int, session: Session = Depends(get_session)) -> Ship:
    """
    Get a ship by its ID.

    Args:
        ship_id (int): The ID of the ship to retrieve.
        session (Session): The database session.
    Returns:
        Ship: The ship object.
    Raises:
        HTTPException: If the ship is not found.
    """
    db_ship = session.get(Ship, ship_id)
    if not db_ship:
        raise HTTPException(
            status_code=404, detail=f"Ship {ship_id} not found")
    return db_ship


@router.put("/{ship_id}", response_model=Ship, tags=["ships"], status_code=status.HTTP_200_OK)
async def update_ship(ship_id: int, ship: Ship, session: Session = Depends(get_session)) -> dict[str, str] | Ship:
    """
    Update a ship by its ID.
    Args:
        ship_id (int): The ID of the ship to update.
        ship (Ship): The updated ship object.
        session (Session): The database session.
    Returns:
        Ship: The updated ship object.
    Raises:
        HTTPException: If the ship is not found.
    """
    db_ship = session.get(Ship, ship_id)
    if not db_ship:
        raise HTTPException(
            status_code=404, detail=f"Ship {ship_id} not found")
    for key, value in ship.model_dump(exclude_unset=True).items():
        setattr(db_ship, key, value)
    session.add(db_ship)
    session.commit()
    session.refresh(db_ship)
    return db_ship


@router.delete("/{ship_id}", tags=["ships"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_ship(ship_id: int, session: Session = Depends(get_session)) -> None:
    """
    Delete a ship by its ID.
    Args:
        ship_id (int): The ID of the ship to delete.
        session (Session): The database session.
    Raises:
        HTTPException: If the ship is not found.
    """
    db_ship = session.get(Ship, ship_id)
    if not db_ship:
        raise HTTPException(
            status_code=404, detail=f"Ship {ship_id} not found")
    session.delete(db_ship)
    session.commit()
    return None


@router.post("/upload-json", tags=["upload"], status_code=status.HTTP_201_CREATED)
async def upload_json(request: Request, session=Depends(get_session)) -> None | dict[str, Any]:
    """
    Import number of ships from JSON file.
    Args:
        request (Request): The incoming request containing the JSON payload.
    Returns:
        dict[str, Any]: A dictionary containing the message and the received JSON data.
    Raises:
        HTTPException: If the JSON data is invalid.
    1. Parse the incoming JSON payload.
    2. Return a success message with the received JSON data.
    3. Raise an HTTPException if the JSON data is invalid.
    4. The function is asynchronous and uses FastAPI's Request object to handle the incoming request.
    5. The function returns a dictionary containing a success message and the received JSON data.
    6. If the JSON data is invalid, it raises an HTTPException with a 400 status code and an error message.
    """
    try:
        # pass
        json_data = await request.json()  # Parse the incoming JSON payload
        # for ship in json_data:
        #    ship_obj = Ship(*ship)
        #    session.add(ship_obj)
        # session.commit()
        # session.refresh(ship_obj)
        return {"message": "JSON received successfully!", "data": ship_obj}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid JSON data"
        )
# ...existing code...
