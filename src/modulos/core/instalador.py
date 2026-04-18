import os
import hashlib
import mysql.connector

class InstaladorModule:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        # Puxa o salt e garante que não seja None
        self.salt = os.getenv('AERIS_SALT', 'aerisdebauruparaomundo')

    
    def validar_seguranca(self, codigo):
        blacklist = ['os.system', 'subprocess.', 'shutil.', 'eval(', 'exec(', 'socket', 'rm -rf']
        for termo in blacklist:
            if termo in codigo:
                return False, f'Termo proibido detectado: {termo}'
        return True, 'Limpo'

    def instalar_skill(self, nome_skill, gatilhos, codigo_fonte):
        aprovado, msg = self.orchestrator.sandbox.validar_sintaxe(codigo_fonte)
        if not aprovado:
            return f'❌ Erro de Sintaxe: {msg}'

        try:
            filename = f'modulo_{nome_skill}.py'
            path = os.path.join(self.orchestrator.diretorio_modulos, filename)
            
            # Padronização absoluta do conteúdo
            conteudo = codigo_fonte.strip()
            
            with open(path, 'w') as f:
                f.write(conteudo)

            # Gerar Hash
            hash_obj = hashlib.sha256(conteudo.encode() + self.salt.encode())
            novo_hash = hash_obj.hexdigest()
            
            # DEBUG: Imprimir para o Mestre conferir
            print(f'-- DEBUG HASH [{nome_skill}]: {novo_hash}')

            conn = self.orchestrator.conectar_db()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM skill_triggers WHERE nome_modulo = %s', (nome_skill,))
            for g in gatilhos:
                cursor.execute('INSERT INTO skill_triggers (gatilho, nome_modulo, hash_integridade) VALUES (%s, %s, %s)', (g, nome_skill, novo_hash))
            conn.commit()
            cursor.close()
            conn.close()

            return f'✅ Skill {nome_skill} instalada e assinada.'
        except Exception as e:
            return f'❌ Erro: {str(e)}'
