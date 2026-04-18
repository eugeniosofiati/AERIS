import os

class SkillModule:
    def __init__(self, orquestrador):
        self.orchestrator = orquestrador
        self.nome = "Motor de Auto-Provisionamento"

    def criar_slot(self, nome_skill, codigo_interno):
        nome_arquivo = f"modulo_{nome_skill.lower()}.py"
        caminho = os.path.join(self.orchestrator.diretorio_modulos, nome_arquivo)
        
        template = f"""
class SkillModule:
    def __init__(self, orquestrador):
        self.orchestrator = orquestrador
        self.nome = "Módulo {nome_skill.capitalize()}"

    def executar(self):
        {codigo_interno}
"""
        try:
            with open(caminho, 'w') as f:
                f.write(template.strip())
            return f"✅ Slot [{nome_skill}] provisionado com sucesso."
        except Exception as e:
            return f"❌ Falha ao criar slot: {e}"

    def executar(self):
        return "Motor de Criação Ativo. Aguardando ordens de expansão do Mestre."
