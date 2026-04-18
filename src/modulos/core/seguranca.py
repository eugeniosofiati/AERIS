import os
from cryptography.fernet import Fernet

class SegurancaMódulo:
    def __init__(self):
        self.nome = "Guardião de Segurança"
        # Busca a chave no ambiente; se não houver, gera uma (apenas para inicialização)
        self.chave = os.getenv('AERIS_SECRET_KEY', Fernet.generate_key().decode())
        self.cipher = Fernet(self.chave.encode())

    def encriptar(self, dado_puro):
        """Transforma texto em AES-256."""
        if not dado_puro: return None
        return self.cipher.encrypt(str(dado_puro).encode()).decode()

    def decriptar(self, dado_cripto):
        """Recupera o texto original."""
        if not dado_cripto: return None
        try:
            return self.cipher.decrypt(dado_cripto.encode()).decode()
        except Exception:
            return "[ERRO DE SEGURANÇA] Falha na decodificação."

    def validar_perimetro(self, path):
        """Exemplo de futura sub-skill: impede acesso fora de /opt/AERIS"""
        return path.startswith("/opt/AERIS") or path.startswith("/app")
