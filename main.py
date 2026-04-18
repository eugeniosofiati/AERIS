import time
import os
from src.orquestrador.orchestrator_aeris import OrchestratorAeris

def run():
    # Inicializa o Cérebro com tratamento de erro para ambiente isolado
    try:
        aeris = OrchestratorAeris()
        print("\n" + "="*40)
        print("🚀 AERIS v1.5.4 - AMBIENTE DOCKER ONLINE")
        print("="*40)
        
        while aeris.running:
            # Em modo container, simulamos o input ou aguardamos comandos via API/Socket
            # Para este teste interativo, usamos o input padrão
            try:
                comando = input("\nMESTRE > ")
                if comando.lower() in ['sair', 'exit']: break
                
                resposta, erro = aeris.pipeline_de_execucao(comando, usuario_id=0)
                print(resposta)
            except EOFError:
                time.sleep(1) # Mantém o container vivo se não houver TTY
    except Exception as e:
        print(f"🚨 FALHA CRÍTICA NO STARTUP: {e}")

if __name__ == "__main__":
    run()
