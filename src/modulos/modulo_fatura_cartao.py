import json
from datetime import datetime

class SkillModule:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def executar(self, argumentos=None):
        if not argumentos:
            return "🚀 Use: fatura_cartao item:valor:categoria"
        
        try:
            itens = argumentos.split()
            processados = []
            
            for registro_cru in itens:
                partes = registro_cru.split(":")
                if len(partes) != 3:
                    continue
                
                nome, valor, cat = partes
                valor_f = float(valor)
                
                dados = {
                    "item": nome,
                    "valor": valor_f,
                    "categoria": cat.lower(),
                    "timestamp": datetime.now().isoformat()
                }
                
                chave = f"fatura_{cat.lower()}_{datetime.now().timestamp()}"
                # Chama o método correto identificado no scanner
                self.orchestrator.contexto.salvar_memoria(0, chave, json.dumps(dados))
                processados.append(f"{nome} (R$ {valor_f:.2f})")

            if not processados:
                return "⚠️ Nenhum item processado. Verifique o formato item:valor:categoria"
                
            # Correção das aspas no join para evitar SyntaxError
            lista_str = ", ".join(processados)
            return f"✅ Sucesso! Itens salvos no DB: {lista_str}"
            
        except Exception as e:
            return f"❌ Erro Crítico: {str(e)}"