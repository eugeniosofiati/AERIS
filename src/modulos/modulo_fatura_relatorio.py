import json
from collections import defaultdict

class SkillModule:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def executar(self, argumentos=None):
        try:
            conn = self.orchestrator.conectar_db()
            cursor = conn.cursor()
            
            # 1. Recuperar todos os registros financeiros e metas
            cursor.execute("SELECT chave FROM contexto_persistente WHERE chave LIKE 'fatura_%'")
            chaves = [row[0] for row in cursor.fetchall()]
            
            if not chaves:
                return "⚠️ Nenhuma informação financeira encontrada no banco."

            gastos_por_cat = defaultdict(float)
            limites_por_cat = {}
            total_geral = 0.0

            # 2. Processamento de dados (Gastos vs Metas)
            for chave in chaves:
                try:
                    conteudo = self.orchestrator.contexto.recuperar_memoria(0, chave)
                    if not conteudo: continue
                    dados = json.loads(conteudo)
                    
                    if "valor_limite" in dados: # É uma meta
                        limites_por_cat[dados["categoria"]] = dados["valor_limite"]
                    elif "valor" in dados: # É um gasto real
                        gastos_por_cat[dados["categoria"]] += dados["valor"]
                        total_geral += dados["valor"]
                except:
                    continue

            # 3. Construção do Painel Visual
            saida = ["📊 PAINEL DE CONTROLE FINANCEIRO AERIS"]
            saida.append("-" * 40)
            
            for cat, gasto in gastos_por_cat.items():
                limite = limites_por_cat.get(cat, 0.0)
                indicador = "⚪" # Sem meta definida
                info_limite = ""
                
                if limite > 0:
                    percent = (gasto / limite) * 100
                    info_limite = f" / R$ {limite:.2f} ({percent:.1f}%)"
                    
                    if percent < 70: indicador = "🟢"
                    elif percent < 100: indicador = "🟡"
                    else: indicador = "🔴"

                saida.append(f" {indicador} {cat.capitalize()}: R$ {gasto:.2f}{info_limite}")
            
            saida.append("-" * 40)
            saida.append(f"💰 TOTAL ACUMULADO: R$ {total_geral:.2f}")
            
            # Alerta Geral
            if any(gastos_por_cat[c] > limites_por_cat.get(c, 999999) for c in gastos_por_cat):
                saida.append("\n⚠️ ATENÇÃO: Você ultrapassou o teto em algumas categorias!")

            return "\n".join(saida)
            
        except Exception as e:
            return f"❌ Erro no Processamento de Inteligência: {str(e)}"