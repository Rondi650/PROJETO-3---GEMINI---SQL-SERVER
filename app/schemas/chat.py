from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated
from datetime import datetime
 
class MensagemChat(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    """Schema de validação para mensagens de chat."""
    
    usuario: Annotated[str, Field(max_length=100)]
    mensagem: str
    origem: Annotated[str, Field(max_length=20)]
    data_hora: datetime
    model: Annotated[str, Field(max_length=100)]
    