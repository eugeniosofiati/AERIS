import hashlib
import os

class SkillModule:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def executar(self, argumentos=None):
        if not argumentos:
            return "❌ Mestre, indique qual intenção devo evoluir (ex: evoluir fatura_cartao)"
        
        nome_skill = argumentos.strip().lower()
        
        # 1. Gerar o código via MEED
        codigo_gerado = self.orchestrator.meed.gerar_esqueleto(nome_skill)
        
        # 2. Usar o Instalador para selar e ativar
        resultado = self.orchestrator.instalador.instalar_skill(
            nome_skill=nome_skill,
            gatilhos=[nome_skill],
            codigo_fonte=codigo_gerado
        )
        
        if "✅" in resultado:
            # 3. Marcar como concluído no banco de dados do MEED
            try:
                conn = self.orchestrator.conectar_db()
                cursor = conn.cursor()
                cursor.execute("UPDATE meed_analise SET status_proposto = %s WHERE comando_tentado = %s", ("skill_criada", nome_skill))
                conn.commit()
                cursor.close()
                conn.close()
            except:
                pass
            
            return f"🧬 [EVOLUÇÃO]: O esqueleto para {nome_skill} foi criado e ativado via Hot-Load."
        
        return resultado