from app.schemas.chat import MensagemChat
from app.core.database import get_connection

class ChatRepository:
    """Gerencia persistência e recuperação de mensagens de chat no banco de dados."""
    
    def __init__(self):
        """
        Inicializa o repositório.
        """
        pass
        
    def salvar_mensagem(self, mensagem: MensagemChat):
        """
        Persiste uma mensagem no banco de dados.
        
        Args:
            mensagem: Objeto MensagemChat a ser salvo
        """
        conn = get_connection()
        try:
            cursor = conn.cursor()
            sql = ("INSERT INTO HistoricoChat "
            "(usuario, mensagem, origem, data_hora, model) "
            "VALUES "
            "(?, ?, ?, ?, ?)")
            cursor.execute(sql, (mensagem.usuario, 
                                 mensagem.mensagem, 
                                 mensagem.origem, 
                                 mensagem.data_hora.isoformat(), 
                                 mensagem.model))
            conn.commit()
        except Exception as e:
            print(f'Erro ao salvar mensagem: {e}')
            conn.rollback()
        finally:
            conn.close()
