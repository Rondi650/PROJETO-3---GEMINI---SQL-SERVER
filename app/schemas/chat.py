from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Literal

class MensagemChat(BaseModel):
    """Schema para validação de mensagens do chat."""
    
    usuario: str = Field(..., min_length=1, description="Nome do usuário")
    mensagem: str = Field(..., min_length=1, description="Conteúdo da mensagem")
    origem: Literal["usuario", "bot"] = Field(..., description="Origem da mensagem")
    data_hora: datetime = Field(default_factory=datetime.now, description="Data e hora da mensagem")
    model: str = Field(..., min_length=1, description="Modelo de IA utilizado")

    @field_validator("mensagem")
    @classmethod
    def validar_mensagem(cls, v: str) -> str:
        """Valida que a mensagem não é apenas espaços em branco."""
        if not v.strip():
            raise ValueError("Mensagem não pode ser vazia ou conter apenas espaços")
        return v.strip()

    @field_validator("usuario")
    @classmethod
    def validar_usuario(cls, v: str) -> str:
        """Valida que o usuário não é vazio."""
        if not v.strip():
            raise ValueError("Usuário não pode ser vazio")
        return v.strip()

    @field_validator("model")
    @classmethod
    def validar_model(cls, v: str) -> str:
        """Valida que o model não é vazio."""
        if not v.strip():
            raise ValueError("Model não pode ser vazio")
        return v.strip()

    model_config = {
        "from_attributes": True,  # Permite conversão de ORM models
        "json_schema_extra": {
            "examples": [
                {
                    "usuario": "João",
                    "mensagem": "Olá, como posso ajudar?",
                    "origem": "usuario",
                    "data_hora": "2024-01-15T10:30:00",
                    "model": "gpt-4o-mini"
                }
            ]
        }
    }
    