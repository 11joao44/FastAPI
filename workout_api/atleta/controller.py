from uuid import uuid4
from fastapi import APIRouter, HTTPException, status, Body
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from workout_api.atleta.models import AtletaModel
from workout_api.atleta.schermas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DataBaseDependency
from pydantic import UUID4

router = APIRouter()

@router.post('/', summary="Criar novo atleta", status_code=status.HTTP_201_CREATED, response_model=AtletaOut)
async def post(db_session: DataBaseDependency, atleta_in: AtletaIn = Body(...)):
    # Verificar se o CPF já existe
    cpf_existente = (await db_session.execute(select(AtletaModel).filter_by(cpf=atleta_in.cpf))).scalars().first()
    if cpf_existente:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, detail=f"Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}")
    
    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome

    categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=categoria_nome))).scalars().first()
    if not categoria:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Categoria '{categoria_nome}' não encontrada")

    centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))).scalars().first()
    if not centro_treinamento:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Centro de treinamento '{centro_treinamento_nome}' não encontrado")

    atleta_out = AtletaOut(id=uuid4(), created_at=datetime.now(), **atleta_in.model_dump())
    atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))
    atleta_model.categoria_id = categoria.pk_id
    atleta_model.centros_treinamento_id = centro_treinamento.pk_id

    try:
        db_session.add(atleta_model)
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_303_SEE_OTHER, detail=f"Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}")

    return atleta_out

@router.get('/', summary='Consultar todos os Atletas', status_code=status.HTTP_200_OK, response_model=list[AtletaOut])
async def query(db_session: DataBaseDependency) -> list[AtletaOut]:
    atletas: list[AtletaModel] = (await db_session.execute(select(AtletaModel))).scalars().all()

    result = []
    for atleta in atletas:
        categoria = (await db_session.execute(select(CategoriaModel).filter_by(pk_id=atleta.categoria_id))).scalars().first()
        centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(pk_id=atleta.centros_treinamento_id))).scalars().first()

        atleta_out = AtletaOut(
            id=atleta.id,
            nome=atleta.nome,
            cpf=atleta.cpf,
            idade=atleta.idade,
            peso=atleta.peso,
            altura=atleta.altura,
            sexo=atleta.sexo,
            created_at=atleta.created_at,
            categoria=categoria,
            centro_treinamento=centro_treinamento
        )
        result.append(atleta_out)

    return result

@router.get('/{id}', summary='Consultar Atleta por ID', status_code=status.HTTP_200_OK, response_model=AtletaOut)
async def query_id(id: UUID4, db_session: DataBaseDependency) -> AtletaOut:
    atleta = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrado com o id: {id}")

    categoria = (await db_session.execute(select(CategoriaModel).filter_by(pk_id=atleta.categoria_id))).scalars().first()
    centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(pk_id=atleta.centros_treinamento_id))).scalars().first()

    atleta_out = AtletaOut(
        id=atleta.id,
        nome=atleta.nome,
        cpf=atleta.cpf,
        idade=atleta.idade,
        peso=atleta.peso,
        altura=atleta.altura,
        sexo=atleta.sexo,
        created_at=atleta.created_at,
        categoria=categoria,
        centro_treinamento=centro_treinamento
    )

    return atleta_out

@router.patch('/{id}', summary='Editar Atleta por ID', status_code=status.HTTP_202_ACCEPTED, response_model=AtletaOut)
async def update_id(id: UUID4, db_session: DataBaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrado com o id: {id}")

    # Atualizar os campos
    update_data = atleta_up.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == 'categoria' and isinstance(value, dict):
            categoria_nome = value.get('nome')
            categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=categoria_nome))).scalars().first()
            if not categoria:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Categoria '{categoria_nome}' não encontrada")
            atleta.categoria_id = categoria.pk_id
        elif key == 'centro_treinamento' and isinstance(value, dict):
            centro_treinamento_nome = value.get('nome')
            centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))).scalars().first()
            if not centro_treinamento:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Centro de treinamento '{centro_treinamento_nome}' não encontrado")
            atleta.centros_treinamento_id = centro_treinamento.pk_id
        else:
            setattr(atleta, key, value)

    await db_session.commit()

    categoria = (await db_session.execute(select(CategoriaModel).filter_by(pk_id=atleta.categoria_id))).scalars().first()
    centro_treinamento = (await db_session.execute(select(CentroTreinamentoModel).filter_by(pk_id=atleta.centros_treinamento_id))).scalars().first()

    atleta_out = AtletaOut(
        id=atleta.id,
        nome=atleta.nome,
        cpf=atleta.cpf,
        idade=atleta.idade,
        peso=atleta.peso,
        altura=atleta.altura,
        sexo=atleta.sexo,
        created_at=atleta.created_at,
        categoria=categoria,
        centro_treinamento=centro_treinamento
    )

    return atleta_out

@router.delete('/{id}', summary='Deletar Atleta por ID', status_code=status.HTTP_204_NO_CONTENT)
async def delete_id(id: UUID4, db_session: DataBaseDependency):
    atleta = (await db_session.execute(select(AtletaModel).filter_by(id=id))).scalars().first()
    
    if not atleta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Atleta não encontrado com o id: {id}")

    await db_session.delete(atleta)
    await db_session.commit()

    return {"message": "Atleta deletado com sucesso"}
