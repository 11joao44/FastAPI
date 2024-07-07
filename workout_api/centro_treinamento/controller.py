from uuid import uuid4
from fastapi import APIRouter, HTTPException, status, Body
from datetime import datetime
from pydantic import UUID4
from sqlalchemy.future import select
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.centro_treinamento.schermas import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.contrib.dependencies import DataBaseDependency

router = APIRouter()

@router.post('/', summary="Criar um novo Centro de treinamento", status_code=status.HTTP_201_CREATED, response_model=CentroTreinamentoOut)
async def post(db_session: DataBaseDependency, centro_treinamento_in: CentroTreinamentoIn = Body(...)) -> CentroTreinamentoOut:
    # Gerar um UUID válido
    centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.dict())
    
    # Criar instância do modelo com os dados de saída
    centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.dict())
    
    db_session.add(centro_treinamento_model)
    await db_session.commit()
    
    return centro_treinamento_out

@router.get('/', summary="Consultar todos os Centros de treinamento", status_code=status.HTTP_200_OK, response_model=list[CentroTreinamentoOut])
async def query(db_session: DataBaseDependency) -> list[CentroTreinamentoOut]:
    centros: list[CentroTreinamentoModel] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    return [CentroTreinamentoOut.model_validate(centro) for centro in centros]

@router.get('/{id}', summary="Consultar Centro de treinamento por ID", status_code=status.HTTP_200_OK, response_model=CentroTreinamentoOut)
async def query_id(id: UUID4, db_session: DataBaseDependency) -> CentroTreinamentoOut:
    centro: CentroTreinamentoModel = (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))).scalars().first()
    if not centro:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Centro de treinamento não encontrado com o id: {id}")
    return CentroTreinamentoOut.model_validate(centro)
