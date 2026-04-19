import json

class SkillModule:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def executar(self, argumentos=None):
        if not argumentos:
            return "⚠️ Uso: fatura_limite Categoria:Valor (Ex: Alimentacao:1500.00)"
        
        try:
            # Parse do argumento
            partes = argumentos.split(':')
            if len(partes) != 2:
                return "❌ Formato inválido. Use Categoria:Valor"
            
            categoria = partes[0].strip().lower()
            limite = float(partes[1].strip())
            
            # Criar objeto de limite
            dados_limite = {
                "tipo": "meta",
                "categoria": categoria,
                "valor_limite": limite
            }
            
            # Salvar no contexto persistente com chave única por categoria
            chave = f"fatura_limite_{categoria}"
            self.orchestrator.contexto.salvar_memoria(0, chave, json.dumps(dados_limite))
            
            return f"✅ Meta estabelecida! Limite para '{categoria.capitalize()}' definido em R$ {limite:.2f}."
            
        except Exception as e:
            return f"❌ Erro ao definir limite: {str(e)}"