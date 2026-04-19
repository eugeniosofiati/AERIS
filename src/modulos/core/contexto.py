import mysql.connector
import os
from datetime import datetime, timedelta, timezone
from cryptography.fernet import Fernet

class ContextoMódulo:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        # Carregamento via Variável de Ambiente para Segurança Volátil
        self.chave_mestra = os.getenv('AERIS_SECRET_KEY')
        if not self.chave_mestra:
            raise ValueError("❌ ERRO CRÍTICO: AERIS_SECRET_KEY não definida no ambiente!")
        self.fernet = Fernet(self.chave_mestra.encode())

    def conectar(self):
        return mysql.connector.connect(
            host=os.getenv('DB_HOST', 'host.docker.internal'),
            user=os.getenv('DB_USER', 'geninho'),
            password=os.getenv('DB_PASSWORD', 'Smg955fd!@'),
            database=os.getenv('DB_NAME', 'aeris_db')
        )

    def salvar_memoria(self, usuario_id, chave, valor, tipo='DADO', horas_vida=None):
        """Salva dados blindados no banco"""
        conn = self.conectar()
        cursor = conn.cursor()
        
        # Blindagem AES-256 (Retorna bytes para o LONGBLOB)
        valor_enc = self.fernet.encrypt(str(valor).encode())

        expiracao = None
        if horas_vida is not None:
            expiracao = datetime.now(timezone.utc) + timedelta(hours=horas_vida)

        sql = """
            INSERT INTO contexto_persistente (usuario_id, chave, valor_blob, tipo, expira_em)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE valor_blob = %s, tipo = %s, expira_em = %s
        """
        
        exp_str = expiracao.strftime('%Y-%m-%d %H:%M:%S') if expiracao else None
        
        # Passamos valor_enc como bytes diretamente
        cursor.execute(sql, (usuario_id, chave, valor_enc, tipo, exp_str, valor_enc, tipo, exp_str))
        
        conn.commit()
        cursor.close()
        conn.close()

    def recuperar_memoria(self, usuario_id, chave):
        """Recupera e decripta dados de forma transparente"""
        conn = self.conectar()
        cursor = conn.cursor()
        
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
            try:
                # Se for string (legado), codificamos; se for bytes, usamos direto
                dado_bruto = res[0]
                if isinstance(dado_bruto, str):
                    dado_bruto = dado_bruto.encode()
                
                return self.fernet.decrypt(dado_bruto).decode()
            except Exception as e:
                return f"Erro na decriptagem: {e}"
        return None

    def executar_garbage_collector(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contexto_persistente WHERE expira_em <= UTC_TIMESTAMP()")
        removidos = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return removidos
