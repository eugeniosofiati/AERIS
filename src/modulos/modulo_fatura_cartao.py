import os

class SkillModule:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def executar(self, argumentos=None):
        if not argumentos or argumentos == "teste_singularidade":
            return "🚀 Módulo de Fatura Ativo. Use: fatura_cartao [item]:[valor]:[categoria]"
        
        try:
            itens = argumentos.split()
            total = 0.0
            detalhes = []
            
            for item in itens:
                partes = item.split(":")
                if len(partes) == 3:
                    nome, valor, cat = partes
                    total += float(valor)
                    detalhes.append(f"  - {nome} ({cat}): R$ {float(valor):.2f}")
            
            if not detalhes:
                return "❌ Formato inválido. Use nome:valor:categoria (ex: Pão:5.50:Alimentação)"

            saida = ["📊 EXTRATO AERIS - FATURA ATUAL"]
            saida.extend(detalhes)
            saida.append("-" * 30)
            saida.append(f"💰 TOTAL: R$ {total:.2f}")
            
            return "\n".join(saida)
        except Exception as e:
            return f"❌ Erro no processamento: {str(e)}"