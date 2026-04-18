class ContextoMódulo:
    def __init__(self, orquestrador):
        self.nome = "Gestor de Memória e Contexto"
        self.orchestrator = orquestrador # Referência para usar o DB e Segurança do Core

    def registrar_fato(self, chave, valor, usuario_id=0):
        """Salva uma informação permanente e encriptada."""
        print(f"[CONTEXTO] Memorizando fato profundo: {chave}")
        return self.orchestrator.salvar_contexto(chave, valor, profundo=True, usuario_id=usuario_id)

    def recuperar_fato(self, chave):
        """Recupera uma informação encriptada do banco."""
        return self.orchestrator.ler_contexto(chave, profundo=True)

    def registrar_sessao(self, chave, valor, usuario_id=0):
        """Salva informação volátil (texto puro)."""
        return self.orchestrator.salvar_contexto(chave, valor, profundo=False, usuario_id=usuario_id)

    def recuperar_sessao(self, chave):
        """Recupera informação volátil."""
        return self.orchestrator.ler_contexto(chave, profundo=False)

    def limpar_sessao(self, usuario_id):
        """Limpa a memória de curto prazo de um usuário específico."""
        conn = self.orchestrator.conectar_db()
        if not conn: return
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contexto_superficial WHERE usuario_id = %s", (usuario_id,))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"[CONTEXTO] Memória superficial do usuário {usuario_id} limpa.")
