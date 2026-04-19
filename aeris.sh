#!/bin/bash

SESSION="aeris_core"
SCRIPT_PATH="/opt/AERIS/aeris.sh"

# --- MODO RECOVERY (Chamado internamente pelo TMUX) ---
if [ "$1" == "--internal-loop" ]; then
    # Redireciona todos os erros do loop para um arquivo de log
    exec 2> /opt/AERIS/aeris_debug.log
    
    BOOTED=false
    while true; do
        if [ "$BOOTED" = false ]; then
            docker exec -it aeris_container python3 src/orquestrador/orchestrator_aeris.py
            BOOTED=true
        else
            clear
            docker exec -it aeris_container python3 src/orquestrador/orchestrator_aeris.py --silent
        fi

        EXIT_CODE=$?
        if [ $EXIT_CODE -eq 0 ]; then
            exit 0
        fi
        sleep 0.5
    done
fi

# --- MODO GESTÃO ---
# 1. Limpa sessões zumbis
tmux kill-session -t $SESSION 2>/dev/null

# 2. Cria e inicia o loop
echo "🚀 Tentando despertar o AERIS..."
tmux new-session -d -s $SESSION "bash $SCRIPT_PATH --internal-loop"

# 3. Pequena pausa para o tmux estabilizar
sleep 0.5

# 4. Tenta conectar
tmux attach -t $SESSION || echo "❌ Erro: A sessão morreu no boot. Verifique 'cat aeris_debug.log'"
