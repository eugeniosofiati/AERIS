import random
import string

class SkillModule:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.descricao = 'Gera senhas seguras aleatórias.'

    def executar(self, argumentos=None):
        try:
            tamanho = int(argumentos) if argumentos and argumentos.strip().isdigit() else 12
            pool = string.ascii_letters + string.digits + '!@#$%&*'
            senha = ''.join(random.choice(pool) for _ in range(tamanho))
            return f'🔐 Senha Gerada ({tamanho} chars): {senha}'
        except Exception as e:
            return f'❌ Erro na geração: {str(e)}'
