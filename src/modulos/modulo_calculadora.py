class SkillModule:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.descricao = "Executa operações matemáticas básicas de forma segura."

    def executar(self, expressao=None):
        if not expressao:
            return "Mestre, por favor forneça uma expressão (ex: 2 + 2)."
        
        try:
            # Sanitização rigorosa para evitar injeção de código
            if not all(char in "0123456789+-*/(). " for char in expressao):
                return "❌ ERRO: Expressão contém caracteres não permitidos por segurança."
            
            # Execução segura sem acesso a funções do sistema
            resultado = eval(expressao, {"__builtins__": None}, {})
            return f"🔢 Resultado: {resultado}"
        except Exception as e:
            return f"❌ ERRO Matemático: {str(e)}"
