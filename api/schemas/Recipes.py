from pydantic import BaseModel, Field


class Recipes(BaseModel) :
    id: int
    title: str
    duration: int
    nbPersons: int
    ownerId: int


class CreateRecipe(BaseModel) :
    title: str = Field(
        min_length=3,
        max_length=100
    )

    duration: int = Field(
        ge=1
    )

    nbPersons: int = Field(
        ge=1
    )


class PatchRecipe(BaseModel) :
    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    duration: int | None = Field(
        default=None,
        ge=1
    )

    nbPersons: int | None = Field(
        default=None,
        ge=1
    )

    ownerId: int | None = Field(
        default=None,
    )


    