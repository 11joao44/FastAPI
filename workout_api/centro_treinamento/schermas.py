from pydantic import UUID4, Field
from typing import Annotated
from workout_api.contrib.schermas import BaseSchema

class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro de treinamento", example="Area 51", max_length=20)]
    endereco: Annotated[str, Field(description="Endereço", example="Rua 12, 329", max_length=60)]
    proprietario: Annotated[str, Field(description="Proprietario", example="João", max_length=30)]

class CentroTreinamentoAtleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do centro de treinamento", example="Area 51", max_length=20)]

class CentroTreinamentoOut(BaseSchema):
    id: Annotated[UUID4, Field(description="Identificador do centro de treinamento")]
    nome: Annotated[str, Field(description="Nome do centro de treinamento", example="Area 51", max_length=20)]
    endereco: Annotated[str, Field(description="Endereço", example="Rua 12, 329", max_length=60)]
    proprietario: Annotated[str, Field(description="Proprietario", example="João", max_length=30)]
