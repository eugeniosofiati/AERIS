#!/bin/bash

# Configurações de Ambiente
SESSION="aeris_web"
PROJECT_DIR="/opt/AERIS"
# Usamos a sua chave de soberania validada
export AERIS_SECRET_KEY="l55uyaVVa6s-03ko_xQ5ls4bU0RA5cazezcim32DnuY="
export AERIS_SALT="aerisdebauruparaomundo"

# Entra na pasta do projeto
cd $PROJECT_DIR

# Verifica se a API já está rodando no TMUX
tmux has-session -t $SESSION 2>/dev/null

if [ $? != 0 ]; then
    echo "🌐 Despertando Interface Web AERIS..."
    # Inicia o FastAPI dentro de uma sessão TMUX para persistência
    tmux new-session -d -s $SESSION "python3 -m src.api.web_bridge"
    echo "✅ Servidor iniciado em segundo plano (Sessão: $SESSION)"
    echo "🔗 Acesse em: http://192.168.5.135:8000"
else
    echo "⚠️ A Interface Web já está ativa."
    echo "💡 Use 'tmux attach -t $SESSION' para ver os logs ou 'tmux kill-session -t $SESSION' para parar."
fi
