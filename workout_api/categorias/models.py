from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from workout_api.contrib.models import BaseModel

class CategoriaModel(BaseModel):
    __tablename__ = 'categorias'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    create_c: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    atleta: Mapped[list['AtletaModel']] = relationship("AtletaModel", back_populates='categoria')
