class SkillModule:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator
    def executar(self, argumentos=None):
        try:
            celsius = float(argumentos)
            f = (celsius * 9/5) + 32
            return f'🌡️ {celsius}°C equivalem a {f}°F'
        except:
            return '❌ Mestre, informe apenas o número em Celsius (ex: temp 25)'