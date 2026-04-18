from src.orquestrador.orchestrator_aeris import OrchestratorAeris

aeris = OrchestratorAeris()

print("\n--- [TESTE 1] Tentativa com Usuário Desconhecido (ID 99) ---")
resultado, erro = aeris.pipeline_de_execucao("ls -la", usuario_id=99)
print(f"Resultado: {resultado} | Erro: {erro}")

print("\n--- [TESTE 2] Tentativa com Mestre Autorizado (ID 0) ---")
resultado, erro = aeris.pipeline_de_execucao("ls -la", usuario_id=0)
print(f"Status do Mestre: {'Sucesso' if not erro else 'Falha'}")
