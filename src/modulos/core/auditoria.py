import mysql.connector
import os
from datetime import datetime, timezone

class AuditoriaMódulo:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def conectar(self):
        return mysql.connector.connect(
            host=os.getenv('DB_HOST', 'host.docker.internal'),
            user=os.getenv('DB_USER', 'geninho'),
            password=os.getenv('DB_PASSWORD', 'Smg955fd!@'),
            database=os.getenv('DB_NAME', 'aeris_db')
        )

    def registrar(self, usuario_id, nivel, acao, recurso, mensagem):
        """Insere um registro permanente na auditoria"""
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            sql = """
                INSERT INTO auditoria_imutavel (usuario_id, nivel, acao, recurso, mensagem)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (usuario_id, nivel, acao, recurso, mensagem))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            # Em auditoria, se o banco falha, imprimimos no log do sistema como última instância
            print(f"⚠️ FALHA CRÍTICA DE AUDITORIA: {e}")

