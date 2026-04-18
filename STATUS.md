# 🚀 PROJETO AERIS - STATUS DO DESENVOLVIMENTO (CONTROLE INTEGRAL)

**Documento de Referência:** v1.5.5 (Skill Telemetry & Hardware Access)  
**Objetivo:** Construir um ecossistema modular, seguro e expansível, centrado na autoridade do Usuário Mestre.  
**Diretriz de Documentação:** Este arquivo deve ser mantido como uma cópia fiel e exaustiva das ações, requisitos e histórico, sem qualquer tipo de síntese ou simplificação.

---

## 🏗️ ARQUITETURA DO ECOSSISTEMA (HÍBRIDA & MODULAR)

### 1. Cérebro Fixo (Core Modules)
Localizados em `src/modulos/core/`. Funções transversais e vitais:
* **estilo.py:** Renderização, limpeza de saída técnica e moldura de resposta (Ativo).
* **seguranca.py:** Gestão de criptografia AES-256 (Fernet) com chave persistente (Ativo).
* **contexto.py:** Gestão de memórias profundas (encriptadas) e superficiais (voláteis) (Ativo).

### 2. Módulos de Skill (20 Slots de Expansão)
Localizados em `src/modulos/modulo_n.py`. Habilidades dinâmicas que podem ser "ensinadas" ao sistema.
* **Mapeamento Dinâmico:** O Orquestrador agora utiliza `importlib` para carregar classes `SkillModule` em tempo de execução sem necessidade de restart do core (Ativo).
* **modulo_status.py:** Primeira Skill de diagnóstico técnico. Realiza leitura de telemetria de hardware (CPU, RAM, Disco) via `psutil` (Ativo - Slot 2).

### 3. Pipeline de 10 Etapas (O Cérebro)
1. **Ingestão:** Recebimento do input e sincronização de estado (Hot-Swap).
2. **Gatekeeper:** Validação de Identidade (DB) e Status (Kill-Switch).
3. **Estado:** Validação de permissões por modo (BASE/PROTECAO/CRIACAO).
4. **Análise de Intenção:** Compreensão semântica (Placeholder).
5. **Seleção de Módulos:** Escolha dinâmica entre os 20 slots via Mapeamento de Gatilhos (Ativo).
6. **Delegação de Skills:** Encaminhamento e instância do módulo carregado (Ativo).
7. **Execução & Sanitização:** Processamento real e filtragem de comandos (Ativo).
8. **QA de Saída:** Validação de segurança do resultado bruto (Placeholder).
9. **Renderização de Estilo:** Formatação final via Módulo Core (Ativo).
10. **Auditoria Imutável:** Registro eterno de toda a cadeia no MySQL (Ativo).

---

## 🛠️ BACKLOG DE DESENVOLVIMENTO (DETALHADO)

### [FASE 0] PREPARAÇÃO E LIMPEZA (GREENFIELD)
- [x] **[INFRA] Purga de Ambiente:** Deleção total do diretório antigo `/opt/AERIS`.
- [x] **[DBA] Reset de Dados:** Deleção da base `aeris_db` e usuários antigos (MySQL 8.0).
- [x] **[INFRA] Novo Repositório:** Recriação do repositório no GitHub com autenticação PAT.
- [x] **[INFRA] Commit Zero:** STATUS.md original enviado ao GitHub.

### [FASE 1] INFRAESTRUTURA & CORE (O Esqueleto)
- [x] **[INFRA] Estrutura Física:** Criação dos diretórios `src`, `config`, `data`, `logs`, `tests`.
- [x] **[INFRA] Dockerização:** Dockerfile (Python 3.11-slim) e `docker-compose.yml` funcionais.
- [x] **[DEV] Fix de Importação:** Injeção de `PYTHONPATH=/app` no ambiente Docker.
- [x] **[DEV] Shutdown Gracioso:** Implementação de `signal.signal` (SIGTERM/SIGINT) - Fim do erro 137.
- [x] **[DEV] Orquestrador Modular:** Classe `OrchestratorAeris` com loop controlado.
- [x] **[DEV] Gestão de Estados:** Polling Ativo de 2 segundos para Hot-Swap reativo via DB.
- [x] **[INFRA] Estrutura Híbrida:** Criação de `src/modulos/core/` e 20 slots de skill.
- [x] **[INFRA] Docker Networking:** Homologação de conectividade entre containers (`agente-redis` e `agente-aeris-core`).

### [FASE 2] BANCO DE DADOS & PERSISTÊNCIA (O Sistema Nervoso)
- [x] **[DBA] Conectividade:** Homologação via `host.docker.internal:3306`.
- [x] **[DBA] Modelagem Relacional:** `usuarios_autorizados`, `auditoria_imutavel`, `contexto_profundo/superficial`.
- [x] **[DBA] Matriz de Autoridade:** Cadastro de Mestre (ID 0) e Visitante (ID 1).
- [x] **[DEV] Core de Contexto:** Implementação do Módulo Core para gestão de fatos e sessões.
- [x] **[DEV] Hardening de Dados:** Implementação de criptografia AES-256 no Módulo Core Segurança. 
- [x] **[QA] Persistência de Chave:** Configuração da `AERIS_SECRET_KEY` no `docker-compose.yml`.
- [x] **[QA] Teste de Hierarquia de Memória:** Validação de gravação/leitura de fatos profundos e variáveis de sessão.
- [ ] **[QA] Teste de Isolamento:** Garantir que Visitantes não leiam Contexto Profundo (Pendente).

### [FASE 3] O AGENTE & PIPELINE DE EXECUÇÃO (O Cérebro)
- [x] **[DEV] Execução & Sanitização:** Integração da Skill de Execução ao Pipeline.
- [x] **[DEV] Auditoria Total:** Registro de tentativas bloqueadas no banco.
- [x] **[DEV] Pipeline 10 Etapas:** Implementação da lógica sequencial no Orquestrador.
- [x] **[DEV] Integração Core Estilo:** Ativação da Etapa 9 para limpeza de saída técnica.
- [x] **[QA] Homologação de Segurança:** Validação de Bypass do Mestre e Bloqueio de ID 1 Inativo.
- [x] **[QA] Homologação Visual:** Validação de saída limpa e emoldurada para o Mestre.
- [x] **[DEV] Mapeamento Dinâmico (Etapa 5 e 6):** Implementação de carregamento de módulos via `importlib.util`.
- [x] **[DEV] Slot de Expansão:** Criação do `modulo_teste.py` como prova de conceito de Hot-Swap.
- [x] **[QA] Homologação Docker Integrada:** Execução bem-sucedida do comando `teste` dentro do container `aeris-v1.5.4`.

### [FASE 4] MELHORIAS, TELEMETRIA & MEED (Evolução)
- [x] **[DEV] Sistema de Telemetria:** Implementação do `modulo_status.py` com leitura de CPU, RAM e Disco (Ativo).
- [x] **[INFRA] Hardening de Container:** Configuração de modo privilegiado e mapeamento de `/proc` para telemetria real.
- [ ] **[DEV] Módulo MEED:** Motor de Evolução e Diagnóstico.
- [ ] **[QA] Teste de Reversibilidade:** Validar Rollback automático para estado BASE.

### [FASE 5] CONECTIVIDADE E INTERFACES (Canais de Entrada)
- [ ] **[DEV] Módulo de Comunicação:** Integração Telegram/WhatsApp.
- [ ] **[DEV] Módulo de Voz:** Processamento Speech-to-Text.
- [ ] **[DEV] Gateway Web:** Painel leve de monitoramento.

### [FASE 6] COGNIÇÃO E INTELIGÊNCIA (Módulos de IA)
- [ ] **[DEV] Integração LLM:** Conexão com modelos de linguagem.
- [ ] **[DEV] Módulo de RAG:** Busca em documentos técnicos locais.

### [FASE 7] AUTOMAÇÃO E CI/CD (Estabilidade Máxima)
- [ ] **[DEV] Módulo de Auto-Update:** Sincronização automática com GitHub.
- [ ] **[DEV] Sistema de Backup:** Backup encriptado automatizado.
- [ ] **[QA] Homologação Final:** Stress test total de todos os sistemas.

---

## 📑 HISTÓRICO DE VALIDAÇÕES TÉCNICAS
* **Snapshot 1.4.6:** Validação do Kill-Switch e Auditoria de tentativas negadas.
* **Snapshot 1.5.0:** Criação física da estrutura modular e implementação lógica do Pipeline.
* **Snapshot 1.5.1:** Criação da Arquitetura Híbrida e Módulo de Estilo.
* **Snapshot 1.5.2:** Ativação do Módulo de Segurança (AES-256) e chave persistente.
* **Snapshot 1.5.3:** Ativação do Módulo de Contexto. Homologação da separação entre memória de longo prazo (encriptada) e curto prazo (volátil).
* **Snapshot 1.5.4:** Implementação do **Mapeamento Dinâmico**. Validação da infraestrutura Docker para suportar injeção de comandos via TTY e carregamento de módulos `SkillModule` sem interrupção do serviço.
* **Snapshot 1.5.5:** Implementação da **Telemetria de Hardware**. Homologação do acesso privilegiado ao Host via container e correção de compatibilidade de leitura de disco em ambiente virtualizado.

---

## 📝 PRÓXIMA AÇÃO (BACKLOG IMEDIATO)
1. Consolidar o motor de **Slots Dinâmicos**: Criar a lógica onde o Orquestrador pode instanciar e deletar novos slots de skill em tempo de execução com base em solicitações complexas do Mestre.
