import os
from src.orquestrador.orchestrator_aeris import OrchestratorAeris

# Simulação de Ambiente (Variáveis que o Orquestrador espera)
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_USER'] = 'root'
os.environ['DB_NAME'] = 'aeris_db'

def testar_mapeamento_dinamico():
    print("\n" + "="*50)
    print("🔍 INICIANDO VALIDAÇÃO DE QA - FASE 3 (MAPEAMENTO)")
    print("="*50)

    try:
        # 1. Instância o Orquestrador atualizado
        aeris = OrchestratorAeris()
        
        # 2. Simula o comando 'teste' vindo do Mestre (ID 0)
        # O Orquestrador deve detectar 'teste', buscar 'modulo_teste.py' e executar.
        print("\n[TESTE] Enviando comando: 'teste'...")
        resultado, erro = aeris.pipeline_de_execucao("teste", usuario_id=0)

        if "Conexão Estabelecida" in resultado:
            print("\n✅ RESULTADO DO ORQUESTRADOR:")
            print(resultado)
            print("\n" + "="*50)
            print("🏆 STATUS QA: APROVADO")
            print("A Etapa 5 (Mapeamento Dinâmico) carregou o Slot 1 com sucesso.")
            print("="*50)
        else:
            print("\n❌ STATUS QA: FALHA")
            print(f"O sistema não retornou a saída esperada do módulo. Saída: {resultado}")

    except Exception as e:
        print(f"\n🚨 ERRO CRÍTICO NO TESTE: {e}")

if __name__ == "__main__":
    testar_mapeamento_dinamico()
