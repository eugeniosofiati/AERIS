import os
import hashlib
import mysql.connector
import time
import signal
from src.modulos.core.estilo import EstiloMódulo
from src.modulos.core.contexto import ContextoMódulo
from src.modulos.core.sandbox import SandboxMódulo
from src.modulos.core.instalador import InstaladorModule
from src.modulos.core.meed import MEEDModule
from src.modulos.core.auditoria import AuditoriaMódulo

class OrchestratorAeris:
    def __init__(self):
        self.running = True
        self.salt = os.getenv("AERIS_SALT", "aerisdebauruparaomundo")
        self.diretorio_modulos = "src/modulos"

        # Instanciação de Módulos Core
        self.estilo = EstiloMódulo()
        self.contexto = ContextoMódulo(self)
        self.sandbox = SandboxMódulo(self)
        self.instalador = InstaladorModule(self)
        self.meed = MEEDModule(self)
        self.auditoria = AuditoriaMódulo(self)

        # Configurações de Identidade
        self.mestre_id = 0
        self.contexto_sistema = {}

        # Sinais de encerramento (Graceful Shutdown)
        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

        # Iniciar Soberania
        self.carregar_soberania()
        
        # Auditoria de Inicialização
        self.auditoria.registrar(self.mestre_id, 'INFO', 'SISTEMA_BOOT', 'CORE', 'Ecossistema AERIS despertou.')

    def conectar_db(self):
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "host.docker.internal"),
            user=os.getenv("DB_USER", "geninho"),
            password=os.getenv("DB_PASSWORD", "Smg955fd!@"),
            database=os.getenv("DB_NAME", "aeris_db")
        )

    def carregar_soberania(self):
        """Valida o Mestre e carrega as diretrizes primárias do banco"""
        conn = None
        try:
            conn = self.conectar_db()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("SELECT nome, role FROM usuarios_autorizados WHERE id = %s AND status = 1", (self.mestre_id,))
            mestre = cursor.fetchone()
            if mestre and mestre['role'] == 'MESTRE':
                print(f"👑 Autoridade Confirmada: Mestre {mestre['nome']}")

            cursor.execute("SELECT chave, valor_blob FROM contexto_persistente WHERE tipo IN ('SISTEMA', 'DIRETRIZ')")
            for row in cursor.fetchall():
                # Tenta decriptar se necessário (usando lógica do módulo contexto se disponível futuramente)
                valor = row['valor_blob'].decode('utf-8') if isinstance(row['valor_blob'], bytes) else row['valor_blob']
                self.contexto_sistema[row['chave']] = valor

            if self.contexto_sistema:
                print(f"🛡️ Diretriz Ativa: {self.contexto_sistema.get('diretriz_primaria', 'Nenhuma')}")

            cursor.close()
        except Exception as e:
            print(f"⚠️ Erro ao carregar soberania: {e}")
        finally:
            if conn: conn.close()

    def stop(self, signum, frame):
        print("\n🛑 Encerrando AERIS (Graceful Shutdown)...")
        self.auditoria.registrar(self.mestre_id, 'AVISO', 'SISTEMA_SHUTDOWN', 'CORE', 'Encerramento solicitado via sinal.')
        self.running = False

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
        self.auditoria.registrar(usuario_id, 'INFO', 'TENTATIVA_EXEC', 'PIPELINE', f"Input: {input_bruto}")
        
        resultado_busca = self.buscar_modulo_por_gatilho(input_bruto)
        if not resultado_busca:
            self.meed.registrar_lacuna(input_bruto, usuario_id)
            self.auditoria.registrar(usuario_id, 'AVISO', 'EXEC_FALHA', 'TRIGGER', f"Gatilho não mapeado: {input_bruto}")
            return self.estilo.formatar_saida(f"Não localizado: {input_bruto}. Intenção registrada.", "SISTEMA"), "NOT_FOUND"

        nome_arquivo, hash_esperado, argumentos = resultado_busca
        caminho_modulo = os.path.join(self.diretorio_modulos, nome_arquivo)

        if os.path.exists(caminho_modulo):
            with open(caminho_modulo, "r") as f:
                conteudo_bruto = f.read().strip()

            hash_calculado = hashlib.sha256(conteudo_bruto.encode() + self.salt.encode()).hexdigest()

            if hash_calculado != hash_esperado:
                self.auditoria.registrar(usuario_id, 'CRÍTICO', 'VIOLACAO_INTEGRIDADE', nome_arquivo, "Hash não confere!")
                return self.estilo.formatar_saida("❌ VIOLAÇÃO DE INTEGRIDADE!", "SISTEMA"), "INTEGRITY_ERROR"

            import importlib.util
            spec = importlib.util.spec_from_file_location("modulo_dinamico", caminho_modulo)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)
            skill = modulo.SkillModule(self)
            
            # Execução e Auditoria de Sucesso
            resultado = skill.executar(argumentos)
            self.auditoria.registrar(usuario_id, 'INFO', 'EXEC_SUCESSO', nome_arquivo, f"Args: {argumentos}")
            return self.estilo.formatar_saida(resultado, "MESTRE"), "SUCCESS"

        self.auditoria.registrar(usuario_id, 'ERRO', 'FILE_MISSING', 'INFRA', f"Arquivo não encontrado: {nome_arquivo}")
        return "Erro físico: arquivo não encontrado.", "FILE_ERROR"

    def run(self):
        print(f"🚀 {self.contexto_sistema.get('projeto_nome', 'AERIS')} Iniciado...")
        while self.running:
            time.sleep(1)
        print("💤 Sistema offline.")

if __name__ == "__main__":
    aeris = OrchestratorAeris()
    aeris.run()
