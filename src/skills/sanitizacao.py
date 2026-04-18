class SanitizacaoSubSkill:
    def __init__(self):
        self.blacklist_visitante = ["rm", "sudo", "apt", "docker", "config"]

    def validar_comando(self, comando, ator):
        if ator == "VISITANTE":
            for proibido in self.blacklist_visitante:
                if proibido in comando.lower():
                    return False, f"[BLOQUEADO] Comando '{proibido}' proibido para VISITANTE."
        return True, None
