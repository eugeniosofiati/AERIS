import mysql.connector
import os
from cryptography.fernet import Fernet

class ContextoMódulo:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        # Recupera a chave mestra das variáveis de ambiente
        self.key = os.getenv('AERIS_SECRET_KEY').encode()
        self.fernet = Fernet(self.key)

    def salvar_memoria(self, usuario_id, chave, valor):
        """Criptografa e persiste um dado no MySQL."""
        conteudo_cifrado = self.fernet.encrypt(str(valor).encode())
        
        try:
            conn = self.orchestrator.conectar_db()
            cursor = conn.cursor()
            query = """
                INSERT INTO contexto_persistente (usuario_id, chave, valor_blob)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE valor_blob = %s
            """
            cursor.execute(query, (usuario_id, chave, conteudo_cifrado, conteudo_cifrado))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao persistir memória: {e}")
            return False

    def recuperar_memoria(self, usuario_id, chave):
        """Recupera e decifra um dado do MySQL."""
        try:
            conn = self.orchestrator.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT valor_blob FROM contexto_persistente WHERE usuario_id = %s AND chave = %s", (usuario_id, chave))
            res = cursor.fetchone()
            cursor.close()
            conn.close()

            if res:
                decifrado = self.fernet.decrypt(res[0]).decode()
                return decifrado
            return None
        except Exception as e:
            print(f"Erro ao recuperar memória: {e}")
            return None
