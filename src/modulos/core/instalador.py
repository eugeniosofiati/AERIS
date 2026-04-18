import os
import hashlib
import mysql.connector

class InstaladorModule:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.salt = os.getenv('AERIS_SALT', 'aerisdebauruparaomundo')

    def instalar_skill(self, nome_skill, gatilhos, codigo_fonte):
        # 1. Validar Sintaxe via Sandbox
        aprovado, msg = self.orchestrator.sandbox.validar_sintaxe(codigo_fonte)
        if not aprovado:
            return f'❌ Erro de Sintaxe: {msg}'

        try:
            # 2. Caminho do arquivo
            filename = f'modulo_{nome_skill}.py'
            path = os.path.join(self.orchestrator.diretorio_modulos, filename)

            # 3. Escrita física
            with open(path, 'w') as f:
                f.write(codigo_fonte.strip())

            # 4. Gerar Hash de Integridade
            hash_obj = hashlib.sha256(codigo_fonte.strip().encode() + self.salt.encode())
            novo_hash = hash_obj.hexdigest()

            # 5. Registrar no Banco de Dados
            conn = self.orchestrator.conectar_db()
            cursor = conn.cursor()
            
            # Limpa gatilhos antigos se existirem
            cursor.execute('DELETE FROM skill_triggers WHERE nome_modulo = %s', (nome_skill,))
            
            # Insere novos gatilhos
            for g in gatilhos:
                sql = "INSERT INTO skill_triggers (gatilho, nome_modulo, hash_integridade) VALUES (%s, %s, %s)"
                cursor.execute(sql, (g, nome_skill, novo_hash))
            
            conn.commit()
            cursor.close()
            conn.close()

            return f'✅ Skill {nome_skill} instalada e assinada com sucesso! Gatilhos: {gatilhos}'

        except Exception as e:
            return f'❌ Erro na instalação: {str(e)}'
