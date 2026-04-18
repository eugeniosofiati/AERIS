class EstiloMódulo:
    def __init__(self):
        self.nome = "Renderizador de Estilo"

    def formatar_saida(self, resultado_bruto, ator):
        """
        Transforma objetos técnicos em texto limpo e elegante.
        """
        # Se for um objeto de execução do sistema (CompletedProcess)
        if hasattr(resultado_bruto, 'stdout'):
            saida = resultado_bruto.stdout
        else:
            saida = str(resultado_bruto)

        if ator == "MESTRE":
            return f"\n{'='*40}\n🚀 AERIS (MESTRE):\n{'-'*40}\n{saida}{'='*40}"
        
        return f"[AERIS]: {saida}"
