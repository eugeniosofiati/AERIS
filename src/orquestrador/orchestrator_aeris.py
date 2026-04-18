import os
import time
import signal
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
        self.contexto = ContextoMódulo(self) # Inicializa o Contexto passando a si mesmo
        self.running = True
        
        signal.signal(signal.SIGTERM, self.finalizar_graciosamente)
        signal.signal(signal.SIGINT, self.finalizar_graciosamente)
        
        self.estado = self.contexto.recuperar_fato("estado_sistema") or "BASE"
        print(f"[SISTEMA] Ecossistema AERIS Online - Modo Ativo: {self.estado}")

    def finalizar_graciosamente(self, signum, frame):
        print(f"\n[SISTEMA] Sinal {signum} recebido. Desligando módulos...")
        self.running = False

    def conectar_db(self):
        try:
            return mysql.connector.connect(
                host=os.getenv('DB_HOST', 'host.docker.internal'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME')
            )
        except mysql.connector.Error:
            return None

    # Métodos base mantidos para suporte aos módulos core
    def ler_contexto(self, chave, profundo=True):
        tabela = "contexto_profundo" if profundo else "contexto_superficial"
        conn = self.conectar_db()
        if not conn: return None
        try:
            cursor = conn.cursor()
            query = f"SELECT valor FROM {tabela} WHERE chave = %s"
            cursor.execute(query, (chave,))
            result = cursor.fetchone()
            valor = result[0] if result else None
            if profundo and valor:
                return self.seguranca.decriptar(valor)
            return valor
        finally:
            if conn:
                cursor.close()
                conn.close()

    def salvar_contexto(self, chave, valor, profundo=True, usuario_id=0):
        tabela = "contexto_profundo" if profundo else "contexto_superficial"
        if profundo:
            valor = self.seguranca.encriptar(valor)
        conn = self.conectar_db()
        if not conn: return
        try:
            cursor = conn.cursor()
            query = f"INSERT INTO {tabela} (usuario_id, chave, valor) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE valor = VALUES(valor)"
            cursor.execute(query, (usuario_id, chave, valor))
            conn.commit()
        finally:
            if conn:
                cursor.close()
                conn.close()

    def registrar_auditoria(self, usuario_id, comando, status, detalhes=None):
        conn = self.conectar_db()
        if not conn: return
        try:
            cursor = conn.cursor()
            query = """INSERT INTO auditoria_imutavel (usuario_id, comando, resultado_status, detalhes_erro) 
                       VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (usuario_id, comando, status, detalhes))
            conn.commit()
        finally:
            if conn:
                cursor.close()
                conn.close()

    def sincronizar_estado(self):
        db_estado = self.contexto.recuperar_fato("estado_sistema")
        if db_estado and db_estado in ["BASE", "PROTECAO", "CRIACAO"]:
            if self.estado != db_estado:
                print(f"[ESTADO] Transição detectada: {self.estado} -> {db_estado}")
                self.estado = db_estado

    def pipeline_de_execucao(self, input_bruto, usuario_id):
        comando = input_bruto
        self.sincronizar_estado()

        conn = self.conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT role, status FROM usuarios_autorizados WHERE id = %s", (usuario_id,))
        res = cursor.fetchone()
        role, status_ativo = res if res else (None, None)
        cursor.close()
        conn.close()

        if not role or status_ativo == 0:
            msg = "[BLOQUEADO] Acesso negado."
            self.registrar_auditoria(usuario_id, comando, "BLOQUEADO", msg)
            return self.estilo.formatar_saida(msg, "DESCONHECIDO"), msg

        if self.estado == "PROTECAO" and role != "MESTRE":
            msg = "[BLOQUEADO] Modo PROTEÇÃO Ativo."
            self.registrar_auditoria(usuario_id, comando, "BLOQUEADO", msg)
            return self.estilo.formatar_saida(msg, role), msg

        # Execução
        resultado, erro = self.executor.executar(comando, role)
        
        # Auditoria e Estilo
        saida_final = self.estilo.formatar_saida(erro or resultado, role)
        self.registrar_auditoria(usuario_id, comando, "ERRO" if erro else "SUCESSO", str(erro or resultado))

        return saida_final, erro

if __name__ == "__main__":
    aeris = OrchestratorAeris()
    while aeris.running:
        aeris.sincronizar_estado()
        time.sleep(2)
