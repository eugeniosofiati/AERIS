import os
import hashlib
import mysql.connector
from src.modulos.core.estilo import EstiloMódulo
from src.modulos.core.contexto import ContextoMódulo
from src.modulos.core.sandbox import SandboxMódulo
from src.modulos.core.instalador import InstaladorModule
from src.modulos.core.meed import MEEDModule

class OrchestratorAeris:
    def __init__(self):
        self.salt = os.getenv("AERIS_SALT", "aerisdebauruparaomundo")
        self.diretorio_modulos = "src/modulos"
        self.estilo = EstiloMódulo()
        self.contexto = ContextoMódulo(self)
        self.sandbox = SandboxMódulo(self)
        self.instalador = InstaladorModule(self)
        self.meed = MEEDModule(self)

    def conectar_db(self):
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "host.docker.internal"),
            user=os.getenv("DB_USER", "geninho"),
            password=os.getenv("DB_PASSWORD", "Smg955fd!@"),
            database=os.getenv("DB_NAME", "aeris_db")
        )

    def buscar_modulo_por_gatilho(self, input_bruto):
        gatilho = input_bruto.split()[0].lower()
        argumentos = " ".join(input_bruto.split()[1:])
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT nome_modulo, hash_integridade FROM skill_triggers WHERE gatilho = %s", (gatilho,))
            res = cursor.fetchone()
            cursor.close()
            conn.close()
            if res:
                return f"modulo_{res[0]}.py", res[1], argumentos
            return None
        except:
            return None

    def pipeline_de_execucao(self, input_bruto, usuario_id=0):
        resultado_busca = self.buscar_modulo_por_gatilho(input_bruto)
        if not resultado_busca:
            self.meed.registrar_lacuna(input_bruto, usuario_id)
            return self.estilo.formatar_saida(f"Não localizado: {input_bruto}. Intenção registrada.", "SISTEMA"), "NOT_FOUND"
        
        nome_arquivo, hash_esperado, argumentos = resultado_busca
        caminho_modulo = os.path.join(self.diretorio_modulos, nome_arquivo)

        if os.path.exists(caminho_modulo):
            with open(caminho_modulo, "r") as f:
                conteudo_bruto = f.read().strip()
            
            hash_calculado = hashlib.sha256(conteudo_bruto.encode() + self.salt.encode()).hexdigest()

            if hash_calculado != hash_esperado:
                return self.estilo.formatar_saida("❌ VIOLAÇÃO DE INTEGRIDADE!", "SISTEMA"), "INTEGRITY_ERROR"

            import importlib.util
            spec = importlib.util.spec_from_file_location("modulo_dinamico", caminho_modulo)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)
            skill = modulo.SkillModule(self)
            return self.estilo.formatar_saida(skill.executar(argumentos), "MESTRE"), "SUCCESS"
        
        return "Erro físico: arquivo não encontrado.", "FILE_ERROR"