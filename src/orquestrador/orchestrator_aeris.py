import os
import importlib.util
from src.skills.execucao import ExecucaoSkill
from src.modulos.core.estilo import EstiloMódulo
from src.modulos.core.seguranca import SegurancaMódulo
from src.modulos.core.contexto import ContextoMódulo

class OrchestratorAeris:
    def __init__(self):
        self.executor = ExecucaoSkill()
        self.estilo = EstiloMódulo()
        self.seguranca = SegurancaMódulo()
        self.contexto = ContextoMódulo(self)
        self.running = True
        self.diretorio_modulos = "src/modulos/"
        self.estado = "BASE" # Fallback direto para teste
        print(f"[SISTEMA] Ecossistema AERIS Online - MODO TESTE ATIVO")

    def conectar_db(self):
        return None # Desativa tentativa de conexão para validação de QA

    def carregar_modulo_dinamico(self, comando):
        trigger = comando.split()[0].lower()
        nome_arquivo = f"modulo_{trigger}.py"
        caminho_completo = os.path.join(self.diretorio_modulos, nome_arquivo)

        if os.path.exists(caminho_completo):
            try:
                spec = importlib.util.spec_from_file_location(trigger, caminho_completo)
                modulo = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(modulo)
                return modulo.SkillModule(self)
            except Exception as e:
                print(f"[ERRO] Falha no slot {trigger}: {e}")
        return None

    def pipeline_de_execucao(self, input_bruto, usuario_id):
        # ETAPA 5: Skill Dinâmica (O foco da nossa entrega)
        skill = self.carregar_modulo_dinamico(input_bruto)
        if skill:
            resultado = skill.executar()
            return self.estilo.formatar_saida(resultado, "MESTRE"), None
        
        return self.estilo.formatar_saida("Comando não reconhecido no mapeamento dinâmico.", "MESTRE"), "NOT_FOUND"
