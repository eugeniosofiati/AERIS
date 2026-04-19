import subprocess
from datetime import datetime
import os

class SkillModule:
    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def executar(self, argumentos=None):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"aeris_db_{timestamp}.sql"
            full_path = f"/app/data/backups/{filename}"
            
            if not os.path.exists("/app/data/backups"):
                os.makedirs("/app/data/backups")

            # Sintaxe oficial para MySQL 8.0.45 (Ubuntu)
            cmd = f"mysqldump --ssl-mode=DISABLED -h host.docker.internal -u geninho -p'Smg955fd!@' aeris_db > {full_path}"
            
            process = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            
            return f"✅ Backup do MySQL 8.0 Local concluído!\n📍 Arquivo: {filename}"
            
        except subprocess.CalledProcessError as e:
            return f"❌ Erro no binário mysqldump: {e.stderr.strip()}"
        except Exception as e:
            return f"❌ Falha sistêmica: {str(e)}"