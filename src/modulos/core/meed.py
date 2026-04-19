import mysql.connector
import os

class MEEDModule:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def registrar_lacuna(self, comando, usuario_id):
        """Registra falhas na tabela meed_analise."""
        try:
            conn = self.orchestrator.conectar_db()
            cursor = conn.cursor()

            sql = """
                INSERT INTO meed_analise (comando_tentado, usuario_id)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE
                    frequencia = frequencia + 1,
                    status_proposto = 'pendente'
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
        """Busca o que o Mestre mais pede e não tem."""
        try:
            conn = self.orchestrator.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT comando_tentado, frequencia FROM meed_analise WHERE status_proposto = 'pendente' AND frequencia >= 2 ORDER BY frequencia DESC")
            sugestoes = cursor.fetchall()
            cursor.close()
            conn.close()

            if sugestoes:
                lista = [f'{cmd} ({freq}x)' for cmd, freq in sugestoes]
                return f'💡 MEED: Sugestão de Skill: { ", ".join(lista) }.'
            return None
        except:
            return None

    def gerar_esqueleto(self, nome_skill):
        return f"class SkillModule:\n    def __init__(self, orchestrator):\n        self.orchestrator = orchestrator\n\n    def executar(self, argumentos=None):\n        return f'🚀 Skill {nome_skill} ativa!'"
