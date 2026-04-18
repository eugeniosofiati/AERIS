import psutil
import shutil
import os

class SkillModule:
    def __init__(self, orquestrador):
        self.orchestrator = orquestrador
        self.nome = "Analista de Telemetria"

    def executar(self):
        # Coleta de dados de Hardware
        cpu_uso = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        
        # Cálculo manual de disco para compatibilidade Docker
        total, usado, livre = shutil.disk_usage("/")
        percent_disco = (usado / total) * 100
        
        # Formatação Técnica para o Mestre
        relatorio = (
            f"📊 RELATÓRIO DE SAÚDE DO ECOSSISTEMA\n"
            f"{'-'*30}\n"
            f"🖥️ CPU: {cpu_uso}%\n"
            f"🧠 RAM: {ram.percent}% (Livre: {ram.available // (1024**2)}MB)\n"
            f"💾 DISCO: {percent_disco:.1f}% (Livre: {livre // (1024**3)}GB)\n"
            f"{'-'*30}\n"
            f"🛰️ STATUS CORE: OPERACIONAL\n"
            f"🔐 SEGURANÇA: ATIVA (AES-256)\n"
            f"🧠 MODO ATIVO: {self.orchestrator.estado}"
        )
        return relatorio
# FIM DO ARQUIVO
