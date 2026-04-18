import subprocess
from src.skills.sanitizacao import SanitizacaoSubSkill

class ExecucaoSkill:
    def __init__(self):
        self.sanitizador = SanitizacaoSubSkill()

    def executar(self, comando, ator):
        autorizado, erro = self.sanitizador.validar_comando(comando, ator)
        if not autorizado:
            return None, erro
        try:
            resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
            return resultado, None
        except Exception as e:
            return None, str(e)
