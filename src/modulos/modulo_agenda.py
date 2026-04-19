class SkillModule:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def executar(self, argumentos=None):
        if not argumentos or argumentos.strip().lower() == "listar":
            return self.listar_agenda()
        
        return self.salvar_agenda(argumentos)

    def listar_agenda(self):
        try:
            conn = self.orchestrator.conectar_db()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT titulo FROM agenda_compromissos WHERE status = 'PENDENTE'")
            res = cursor.fetchall()
            cursor.close()
            conn.close()
            
            if not res:
                return "📅 Mestre, sua agenda está vazia no momento."
            
            itens = "\n".join([f"• {r['titulo']}" for r in res])
            return f"📅 Seus compromissos pendentes:\n{itens}"
        except Exception as e:
            return f"❌ Erro ao ler agenda: {e}"

    def salvar_agenda(self, texto):
        try:
            conn = self.orchestrator.conectar_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO agenda_compromissos (titulo) VALUES (%s)", (texto,))
            conn.commit()
            cursor.close()
            conn.close()
            return f"✅ Agendado com sucesso: {texto}"
        except Exception as e:
            return f"❌ Erro ao salvar na agenda: {e}"
