from app.models.chat import HistoricoChat
from app.schemas.chat import MensagemChat

class ChatRepository:
    def __init__(self, db_session):
        self.db = db_session
        
    def salvar_mensagem(self, mensagem: MensagemChat):
        registro = HistoricoChat(**mensagem.dict())
        self.db.add(registro)
        self.db.commit()
        
    def obter_historico(self, usuario=None):
        query = self.db.query(HistoricoChat)
        if usuario:
            query = query.filter(HistoricoChat.usuario == usuario)
        return query.order_by(HistoricoChat.data_hora).all()