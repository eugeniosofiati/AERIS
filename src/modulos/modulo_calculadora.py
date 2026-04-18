import re

class SkillModule:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
        self.descricao = 'Calculadora com suporte a variáveis persistentes.'

    def executar(self, argumentos=None):
        if not argumentos:
            return 'Mestre, use: calc <expressão> ou calc set <nome> = <valor>'

        usuario_id = 0 # Fixo para o Mestre nesta fase

        try:
            # --- LÓGICA DE ATRIBUIÇÃO (SET) ---
            if argumentos.startswith('set '):
                match = re.search(r'set\s+(\w+)\s*=\s*(.+)', argumentos)
                if match:
                    chave = f'var_{match.group(1)}'
                    valor = match.group(2)
                    # Resolve o valor antes de salvar (ex: set x = 2+2 salva 4)
                    resultado_valor = eval(valor, {'__builtins__': None}, {})
                    self.orchestrator.contexto.salvar_memoria(usuario_id, chave, resultado_valor)
                    return f'🧠 Variável {match.group(1)} salva com valor: {resultado_valor}'

            # --- LÓGICA DE CÁLCULO COM RECUPERAÇÃO ---
            # Busca todas as variáveis do usuário no banco (simplificado para o teste)
            # Para este MVP, vamos permitir que o eval use variáveis salvas
            
            # Sanitização de segurança
            if not all(char in '0123456789+-*/(). abcdefghijklmnopqrstuvwxyz_' for char in argumentos.lower()):
                return '❌ ERRO: Caracteres ilegais detectados.'

            # Tenta encontrar nomes de variáveis na expressão e substitui pelos valores do DB
            palavras = re.findall(r'[a-zA-Z_]\w*', argumentos)
            contexto_vars = {}
            for p in palavras:
                val = self.orchestrator.contexto.recuperar_memoria(usuario_id, f'var_{p}')
                if val is not None:
                    contexto_vars[p] = float(val)

            resultado = eval(argumentos, {'__builtins__': None}, contexto_vars)
            return f'🔢 Resultado: {resultado}'

        except Exception as e:
            return f'❌ Erro: {str(e)}'
