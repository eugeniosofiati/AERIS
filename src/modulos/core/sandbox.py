import ast

class SandboxMódulo:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def validar_sintaxe(self, codigo):
        """Verifica se o código Python é válido antes de salvar."""
        try:
            ast.parse(codigo)
            return True, "✅ Sintaxe aprovada."
        except SyntaxError as e:
            erro_msg = f"❌ Erro de Sintaxe: {e.msg} (Linha {e.lineno})"
            return False, erro_msg
        except Exception as e:
            return False, f"❌ Erro inesperado na validação: {str(e)}"
