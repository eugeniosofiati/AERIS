import json
from collections import defaultdict

class SkillModule:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def executar(self, argumentos=None):
        try:
            # 1. Buscar chaves via SQL direto
            conn = self.orchestrator.conectar_db()
            cursor = conn.cursor()
            cursor.execute("SELECT chave FROM contexto_persistente WHERE chave LIKE 'fatura_%'")
            chaves = [row[0] for row in cursor.fetchall()]
            
            if not chaves:
                return "⚠️ Nenhuma fatura encontrada."

            categorias = defaultdict(float)
            total_geral = 0.0
            contagem = 0

            # 2. Usar o método recuperar_memoria do Core com segurança
            for chave in chaves:
                try:
                    # Garantimos que a chave seja uma string limpa
                    chave_str = str(chave).strip()
                    conteudo = self.orchestrator.contexto.recuperar_memoria(0, chave_str)
                    
                    if conteudo:
                        # Se o Core retornar bytes, decodificamos aqui
                        if isinstance(conteudo, bytes):
                            conteudo = conteudo.decode('utf-8')
                        
                        dados = json.loads(conteudo)
                        valor = dados.get("valor", 0)
                        cat = dados.get("categoria", "sem categoria")
                        
                        categorias[cat] += valor
                        total_geral += valor
                        contagem += 1
                except Exception:
                    continue

            # 3. Formatar Saída
            saida = ["📊 RELATÓRIO CONSOLIDADO AERIS"]
            if not categorias:
                return "⚠️ Dados encontrados, mas não puderam ser descriptografados. Verifique o SALT."
                
            for cat, total in categorias.items():
                saida.append(f"  • {cat.capitalize()}: R$ {total:.2f}")
            
            saida.append("-" * 35)
            saida.append(f"💰 TOTAL ({contagem} itens): R$ {total_geral:.2f}")
            
            return "\n".join(saida)
            
        except Exception as e:
            return f"❌ Erro Crítico no Relatório: {str(e)}"