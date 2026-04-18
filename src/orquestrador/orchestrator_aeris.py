import os
import importlib.util
import mysql.connector
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
        self.diretorio_modulos = "src/modulos/"
        self.estado = "BASE"
        
    def conectar_db(self):
        return mysql.connector.connect(
            host=os.getenv('DB_HOST', 'host.docker.internal'),
            user=os.getenv('DB_USER', 'geninho'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'aeris_db')
        )

    def registrar_auditoria(self, usuario_id, comando, status, erro=None):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            sql = "INSERT INTO auditoria_imutavel (usuario_id, comando, resultado_status, detalhes_erro) VALUES (%s, %s, %s, %s)"
            status_enum = 'SUCESSO' if status == 'SUCCESS' else 'ERRO'
            cursor.execute(sql, (usuario_id, comando, status_enum, str(erro) if erro else None))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"[ERRO AUDITORIA]: {e}")

    def buscar_modulo_por_gatilho(self, comando):
        trigger_input = comando.split()[0].lower()
        nome_arquivo_alvo = None
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT nome_modulo FROM skill_triggers WHERE gatilho = %s", (trigger_input,))
            res = cursor.fetchone()
            if res:
                nome_arquivo_alvo = f"modulo_{res[0]}.py"
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"[ERRO DB TRIGGERS]: {e}")
        return nome_arquivo_alvo

    def carregar_modulo_dinamico(self, nome_arquivo):
        if not nome_arquivo: return None
        caminho_completo = os.path.join(self.diretorio_modulos, nome_arquivo)
        if os.path.exists(caminho_completo):
            trigger_name = nome_arquivo.replace("modulo_", "").replace(".py", "")
            spec = importlib.util.spec_from_file_location(trigger_name, caminho_completo)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)
            return modulo.SkillModule(self)
        return None

    def pipeline_de_execucao(self, input_bruto, usuario_id):
        status = "SUCCESS"
        erro_log = None
        
        # Nova Etapa 5: Tradução de Gatilho para Módulo
        nome_arquivo = self.buscar_modulo_por_gatilho(input_bruto)
        skill = self.carregar_modulo_dinamico(nome_arquivo)
        
        if skill:
            resultado = skill.executar()
            resposta_final = self.estilo.formatar_saida(resultado, "MESTRE")
        else:
            status = "ERRO"
            msg = f"Habilidade '{input_bruto}' não localizada. Deseja que eu a desenvolva?"
            resposta_final = self.estilo.formatar_saida(msg, "SISTEMA")

        self.registrar_auditoria(usuario_id, input_bruto, status, erro_log)
        return resposta_final, erro_log
