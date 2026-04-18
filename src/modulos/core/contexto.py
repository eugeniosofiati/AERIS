import mysql.connector
import os
from datetime import datetime, timedelta, timezone
from cryptography.fernet import Fernet

class ContextoMódulo:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.chave_mestra = os.getenv('AERIS_SECRET_KEY')
        self.fernet = Fernet(self.chave_mestra.encode())

    def conectar(self):
        return mysql.connector.connect(
            host=os.getenv('DB_HOST', 'host.docker.internal'),
            user=os.getenv('DB_USER', 'geninho'),
            password=os.getenv('DB_PASSWORD', 'Smg955fd!@'),
            database=os.getenv('DB_NAME', 'aeris_db')
        )

    def salvar_memoria(self, usuario_id, chave, valor, horas_vida=None):
        conn = self.conectar()
        cursor = conn.cursor()
        valor_enc = self.fernet.encrypt(str(valor).encode()).decode()
        
        expiracao = None
        if horas_vida is not None:
            # Usando UTC explícito para evitar erro de Timezone
            expiracao = datetime.now(timezone.utc) + timedelta(hours=horas_vida)

        sql = """
            INSERT INTO contexto_persistente (usuario_id, chave, valor_blob, expira_em) 
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE valor_blob = %s, expira_em = %s
        """
        # Convertemos para string para o MySQL aceitar sem confusão
        exp_str = expiracao.strftime('%Y-%m-%d %H:%M:%S') if expiracao else None
        
        cursor.execute(sql, (usuario_id, chave, valor_enc, exp_str, valor_enc, exp_str))
        conn.commit()
        cursor.close()
        conn.close()

    def recuperar_memoria(self, usuario_id, chave):
        conn = self.conectar()
        cursor = conn.cursor()
        # Comparamos com UTC_TIMESTAMP do MySQL
        sql = """
            SELECT valor_blob FROM contexto_persistente 
            WHERE usuario_id = %s AND chave = %s 
            AND (expira_em IS NULL OR expira_em > UTC_TIMESTAMP())
        """
        cursor.execute(sql, (usuario_id, chave))
        res = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if res:
            return self.fernet.decrypt(res[0] if isinstance(res[0], bytes) else res[0].encode()).decode()
        return None

    def executar_garbage_collector(self):
        conn = self.conectar()
        cursor = conn.cursor()
        # Limpa tudo que for menor ou igual ao horário atual UTC
        cursor.execute("DELETE FROM contexto_persistente WHERE expira_em <= UTC_TIMESTAMP()")
        removidos = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return removidos
