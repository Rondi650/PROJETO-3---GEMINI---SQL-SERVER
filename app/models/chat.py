from sqlalchemy import  String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
 
class Base(DeclarativeBase):
    pass
 
class HistoricoChat(Base):
    __tablename__ = 'HistoricoChat'
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    usuario: Mapped[str] = mapped_column(String(100), nullable=False)
    mensagem: Mapped[str] = mapped_column(String)
    origem: Mapped[str] = mapped_column(String(20), nullable=False)
    data_hora: Mapped[DateTime] = mapped_column(nullable=False)
