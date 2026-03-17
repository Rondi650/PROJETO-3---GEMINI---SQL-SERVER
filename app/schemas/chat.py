from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime
 
class MensagemChat(BaseModel):
    """Schema de validação para mensagens de chat."""
    
    usuario: Annotated[str, Field(max_length=100)]
    mensagem: str
    origem: Annotated[str, Field(max_length=20)]
    data_hora: datetime
    model: Annotated[str, Field(max_length=100)]
    