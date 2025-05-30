from sqlmodel import Field, SQLModel


class Ship(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    classification: str = Field(index=True)
    sign: str | None = Field(default=None, index=True)
    speed: str | None = Field(default=None, index=True)
    captain: str | None = Field(default=None, index=True)
    comment: str | None = Field(default=None, index=True)
    url: str | None = Field(default=None, index=False)
