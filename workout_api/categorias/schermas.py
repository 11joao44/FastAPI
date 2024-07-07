from pydantic import UUID4, Field
from typing import Annotated
from workout_api.contrib.schermas import BaseSchema

class CategoriaIn(BaseSchema):
    nome: Annotated[str, Field(description="Nome da categoria", example="Scale", max_length=10)]

class CategoriaOut(CategoriaIn):
    id: Annotated[UUID4, Field(description="Identificador da categoria")]
