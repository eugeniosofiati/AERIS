import os
import hashlib
import mysql.connector
import time
import signal
import sys

# Módulos Core
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
        
        # Modo Silencioso: Ativado se o sistema for reiniciado por queda de conexão
        self.silent_mode = "--silent" in sys.argv

        if hasattr(signal, "SIGWINCH"): signal.signal(signal.SIGWINCH, signal.SIG_IGN)

        self.estilo = EstiloMódulo()
        self.contexto = ContextoMódulo(self)
        self.sandbox = SandboxMódulo(self)
        self.instalador = InstaladorModule(self)
        self.meed = MEEDModule(self)
        self.auditoria = AuditoriaMódulo(self)

        self.mestre_id = 0
        self.contexto_sistema = {}

        signal.signal(signal.SIGINT, self.handle_exit)
        signal.signal(signal.SIGTERM, self.handle_exit)

        self.carregar_soberania()
        
        if not self.silent_mode:
            self.auditoria.registrar(self.mestre_id, 'INFO', 'SISTEMA_BOOT', 'CORE', 'Ecossistema AERIS despertou.')

    def conectar_db(self):
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "host.docker.internal"),
            user=os.getenv("DB_USER", "geninho"),
            password=os.getenv("DB_PASSWORD", "Smg955fd!@"),
            database=os.getenv("DB_NAME", "aeris_db")
        )

    def carregar_soberania(self):
        conn = None
        try:
            conn = self.conectar_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT nome, role FROM usuarios_autorizados WHERE id = %s AND status = 1", (self.mestre_id,))
            mestre = cursor.fetchone()
            
            # Só imprime a autoridade no primeiro boot
            if mestre and not self.silent_mode: 
                print(f"👑 Autoridade Confirmada: Mestre {mestre['nome']}")
                
            cursor.execute("SELECT chave, valor_blob FROM contexto_persistente WHERE tipo IN ('SISTEMA', 'DIRETRIZ')")
            for row in cursor.fetchall():
                valor = row['valor_blob'].decode('utf-8') if isinstance(row['valor_blob'], bytes) else row['valor_blob']
                self.contexto_sistema[row['chave']] = valor
            
            if self.contexto_sistema and not self.silent_mode: 
                print(f"🛡️ Diretriz Ativa: {self.contexto_sistema.get('diretriz_primaria', 'Nenhuma')}")
                
            cursor.close()
        except: pass
        finally:
            if conn: conn.close()

    def handle_exit(self, signum, frame):
        self.stop(exit_code=1)

    def stop(self, exit_code=0):
        if not self.running: return
        if exit_code == 0:
            print("\n👋 Até logo, Mestre Geninho!")
        self.running = False
        sys.exit(exit_code)

    def buscar_modulo_por_gatilho(self, input_bruto):
        partes = input_bruto.split()
        if not partes: return None
        gatilho = partes[0].lower()
        argumentos = " ".join(partes[1:])
        try:
            conn = self.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT nome_modulo, hash_integridade FROM skill_triggers WHERE gatilho = %s", (gatilho,))
            res = cursor.fetchone()
            cursor.close()
            conn.close()
            if res: return f"modulo_{res[0]}.py", res[1], argumentos
            return None
        except: return None

    def pipeline_de_execucao(self, input_bruto, usuario_id=0):
        resultado_busca = self.buscar_modulo_por_gatilho(input_bruto)
        if not resultado_busca:
            self.meed.registrar_lacuna(input_bruto, usuario_id)
            return self.estilo.formatar_saida(f"Não localizado: {input_bruto}. Intenção registrada no MEED.", "SISTEMA"), "NOT_FOUND"

        nome_arquivo, hash_esperado, argumentos = resultado_busca
        caminho_modulo = os.path.join(self.diretorio_modulos, nome_arquivo)

        if os.path.exists(caminho_modulo):
            with open(caminho_modulo, "r") as f:
                conteudo = f.read().strip()
            hash_calculado = hashlib.sha256(conteudo.encode() + self.salt.encode()).hexdigest()
            if hash_calculado != hash_esperado:
                return self.estilo.formatar_saida("❌ VIOLAÇÃO DE INTEGRIDADE!", "SISTEMA"), "INTEGRITY_ERROR"
            import importlib.util
            spec = importlib.util.spec_from_file_location("mod", caminho_modulo)
            modulo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(modulo)
            skill = modulo.SkillModule(self)
            return self.estilo.formatar_saida(skill.executar(argumentos), "MESTRE"), "SUCCESS"
        return "Erro físico.", "FILE_ERROR"

    def run(self):
        if not self.silent_mode:
            print(f"🚀 {self.contexto_sistema.get('projeto_nome', 'AERIS')} Iniciado...")
            
        while self.running:
            try:
                sys.stdout.flush()
                comando = input("👑 AERIS > ").strip()
                if not comando: continue

                if comando.lower() in ["sair", "exit", "tchau", "tchau aeris", "tchau, aeris"]:
                    self.stop(exit_code=0) 

                resultado, _ = self.pipeline_de_execucao(comando)
                print(resultado)

            except EOFError:
                # Se a conexão cair, sai com 1 para o shell reiniciar silenciosamente
                sys.exit(1)
            except KeyboardInterrupt:
                self.stop(exit_code=1)
            except Exception as e:
                print(f"⚠️ Erro: {e}")
                time.sleep(0.1)

if __name__ == "__main__":
    aeris = OrchestratorAeris()
    aeris.run()
