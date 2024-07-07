from fastapi import APIRouter, HTTPException, status, Body
from pydantic import UUID4
from sqlalchemy.future import select
from uuid import uuid4

from workout_api.categorias.schermas import CategoriaIn, CategoriaOut
from workout_api.categorias.models import CategoriaModel
from workout_api.contrib.dependencies import DataBaseDependency

router = APIRouter()

@router.post('/', summary="Criar uma nova categoria", status_code=status.HTTP_201_CREATED, response_model=CategoriaOut)
async def post(db_session: DataBaseDependency, categoria_in: CategoriaIn = Body(...)) -> CategoriaOut:
    categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())
    db_session.add(categoria_model)
    await db_session.commit()
    return categoria_out

@router.get('/', summary="Consultar todas as categorias", status_code=status.HTTP_200_OK, response_model=list[CategoriaOut])
async def query(db_session: DataBaseDependency) -> list[CategoriaOut]:
    categorias: list[CategoriaModel] = (await db_session.execute(select(CategoriaModel))).scalars().all()
    return [CategoriaOut.model_validate(categoria) for categoria in categorias]

@router.get('/{id}', summary="Consultar categoria por id", status_code=status.HTTP_200_OK, response_model=CategoriaOut)
async def query_id(id: UUID4, db_session: DataBaseDependency) -> CategoriaOut:
    categoria: CategoriaModel = (await db_session.execute(select(CategoriaModel).filter_by(id=id))).scalars().first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Categoria não encontrada com o id: {id}")
    return CategoriaOut.model_validate(categoria)
