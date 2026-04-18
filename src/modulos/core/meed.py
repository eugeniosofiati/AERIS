import mysql.connector
import os

class MEEDModule:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def registrar_lacuna(self, comando, usuario_id):
        """Registra um comando que o sistema não soube resolver."""
        try:
            conn = self.orchestrator.conectar_db()
            cursor = conn.cursor()
            
            sql = """
                INSERT INTO meed_analise (comando_tentado, usuario_id)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE 
                    frequencia = frequencia + 1,
                    status_proposto = 'em_analise'
            """
            cursor.execute(sql, (comando, usuario_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f'[MEED ERR]: {e}')
            return False

    def sugerir_expansao(self):
        """Analisa comandos frequentes e sugere criação ao Mestre."""
        try:
            conn = self.orchestrator.conectar_db()
            cursor = conn.cursor()
            # Busca comandos que falharam mais de 2 vezes
            cursor.execute("SELECT comando_tentado, frequencia FROM meed_analise WHERE status_proposto != 'skill_criada' AND frequencia >= 2 ORDER BY frequencia DESC")
            sugestoes = cursor.fetchall()
            cursor.close()
            conn.close()
            
            if sugestoes:
                lista = [f'{cmd} ({freq}x)' for cmd, freq in sugestoes]
                return f'💡 MEED: Notei interesse recorrente em: { ", ".join(lista) }. Deseja converter em Skill?'
            return None
        except:
            return None
