import os
import re
import hashlib
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
        # SALT RECUPERADO DA VARIÁVEL DE AMBIENTE DO DOCKER
        self.__salt = os.getenv('AERIS_SALT', '') 
        
    def conectar_db(self):
        return mysql.connector.connect(
            host=os.getenv('DB_HOST', 'host.docker.internal'),
            user=os.getenv('DB_USER', 'geninho'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'aeris_db')
        )

    def calcular_hash_modulo(self, caminho_arquivo):
        try:
            with open(caminho_arquivo, "rb") as f:
                conteudo = f.read()
            assinatura = conteudo + self.__salt.encode()
            return hashlib.sha256(assinatura).hexdigest()
        except:
            return None

    def buscar_role_usuario(self, usuario_id):
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM usuarios_autorizados WHERE id = %s AND status = 1", (usuario_id,))
            res = cursor.fetchone()
            cursor.close()
            conn.close()
            return res[0] if res else None
        except:
            return None

    def buscar_modulo_por_gatilho(self, comando):
        trigger_input = comando.split()[0].lower()
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT nome_modulo, hash_integridade FROM skill_triggers WHERE gatilho = %s", (trigger_input,))
            res = cursor.fetchone()
            cursor.close()
            conn.close()
            if res:
                return f"modulo_{res[0]}.py", res[1]
        except:
            return None, None

    def carregar_modulo_dinamico(self, nome_arquivo, hash_esperado):
        if not nome_arquivo: return None
        caminho_completo = os.path.join(self.diretorio_modulos, nome_arquivo)
        
        if os.path.exists(caminho_completo):
            # VALIDAÇÃO DE INTEGRIDADE
            hash_atual = self.calcular_hash_modulo(caminho_completo)
            if hash_esperado and hash_atual != hash_esperado:
                return "ERR_INTEGRITY"
            
            spec = importlib.util.spec_from_file_location("mod", caminho_completo)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)
            return modulo.SkillModule(self)
        return None

    def pipeline_de_execucao(self, input_bruto, usuario_id):
        # Etapa 2: Gatekeeper
        role = self.buscar_role_usuario(usuario_id)
        if not role:
            return self.estilo.formatar_saida("Acesso Negado.", "SISTEMA"), "FORBIDDEN"

        # Etapa 5: Seleção e Etapa 4: Integridade
        nome_arquivo, hash_esperado = self.buscar_modulo_por_gatilho(input_bruto)
        skill = self.carregar_modulo_dinamico(nome_arquivo, hash_esperado)
        
        if skill == "ERR_INTEGRITY":
            return self.estilo.formatar_saida("❌ VIOLAÇÃO DE INTEGRIDADE!", "SISTEMA"), "SEC_ERR"
        
        if skill:
            try:
                # Restrição Mestre
                if "status" in nome_arquivo and role != "MESTRE":
                    return self.estilo.formatar_saida("Nível insuficiente.", "SISTEMA"), "UNAUTHORIZED"
                
                resultado = skill.executar()
                # Etapa 8: QA de Saída (Filtro simples integrado)
                if any(x in str(resultado) for x in ["Password", "Smg955fd!@"]):
                    resultado = "[CONTEÚDO SENSÍVEL FILTRADO]"
                
                return self.estilo.formatar_saida(resultado, "MESTRE"), None
            except Exception as e:
                return self.estilo.formatar_saida(f"Erro: {e}", "SISTEMA"), "ERR"
        
        return self.estilo.formatar_saida(f"Não localizado: {input_bruto}", "SISTEMA"), "NOT_FOUND"
