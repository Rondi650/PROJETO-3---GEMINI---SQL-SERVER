from app.models.chat import HistoricoChat
from app.schemas.chat import MensagemChat

class ChatRepository:
    """Gerencia persistência e recuperação de mensagens de chat no banco de dados."""
    
    def __init__(self, db_session):
        """
        Inicializa o repositório com uma sessão do SQLAlchemy.
        
        Args:
            db_session: Sessão ativa do banco de dados
        """
        self.db = db_session
        
    def salvar_mensagem(self, mensagem: MensagemChat):
        """
        Persiste uma mensagem no banco de dados.
        
        Args:
            mensagem: Objeto MensagemChat a ser salvo
        """
        registro = HistoricoChat(**mensagem.dict())
        try:
            self.db.add(registro)
            self.db.commit()
        except Exception as e:
            print(f'Erro ao salvar mensagem: {e}')
            self.db.rollback()
        
    def obter_historico(self, usuario=None):
        """
        Recupera histórico de mensagens do banco de dados.
        
        Args:
            usuario: Filtro opcional por nome de usuário
        
        Returns:
            Lista de mensagens ordenadas por data/hora
        """
        query = self.db.query(HistoricoChat)
        if usuario:
            query = query.filter(HistoricoChat.usuario == usuario)
        return query.order_by(HistoricoChat.data_hora).all()
