from pydantic import UUID4, Field, PositiveFloat
from typing import Annotated, Optional
from workout_api.categorias.schermas import CategoriaIn
from workout_api.centro_treinamento.schermas import CentroTreinamentoAtleta
from workout_api.contrib.schermas import BaseSchema, OutMixin


class Atleta(BaseSchema):
    nome: Annotated[str, Field(description="Nome do atleta", example="João", max_length=50)]
    cpf: Annotated[str, Field(description="CPF do atleta", example="07202642190", max_length=11)]
    idade: Annotated[int, Field(description="Idade do atleta", example=24)]
    peso: Annotated[PositiveFloat, Field(description="Peso do atleta", example=74.83)]
    altura: Annotated[PositiveFloat, Field(description="Altura do atleta", example=1.70)]
    sexo: Annotated[str, Field(description="Sexo do atleta", example="M", max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description="Categoria do atleta")]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description="Centro de treinamento do atleta")]

class AtletaIn(Atleta):
    pass

class AtletaOut(Atleta, OutMixin):
    pass

class AtletaUpdate(BaseSchema):
    nome: Optional[str] = Field(None, description="Nome do atleta", example="João", max_length=50)
    idade: Optional[int] = Field(None, description="Idade do atleta", example=24)
    categoria: Optional[CategoriaIn] = Field(None, description="Categoria do atleta")
    centro_treinamento: Optional[CentroTreinamentoAtleta] = Field(None, description="Centro de treinamento do atleta")
