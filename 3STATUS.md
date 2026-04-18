# 🚀 PROJETO AERIS - STATUS DO DESENVOLVIMENTO (CONTROLE INTEGRAL)

**Documento de Referência:** v1.4.5 (Active Hot-Swap & Boot Logic Fixed)  
**Objetivo:** Construir um ecossistema modular, seguro e expansível, centrado na autoridade do Usuário Mestre.  
**Diretriz de Documentação:** Este arquivo deve ser mantido como uma cópia fiel e exaustiva das ações, requisitos e histórico, sem qualquer tipo de síntese ou simplificação. Se o assistente perder o contexto, o conteúdo anterior deve ser reenviado pelo usuário para reintegração.

---

## 🏗️ ARQUITETURA DO ECOSSISTEMA
O AERIS opera sob um modelo de **Orquestração Modular**, onde o núcleo central coordena 20 sistemas independentes através de um pipeline de 10 etapas. Nenhuma ação é executada sem passar pelos filtros de Segurança e Coerência.

### Hierarquia de Componentes:
1. **Orquestrador:** Cérebro executivo (Ativo em container Docker). Gerencia Estados (BASE, PROTECAO, CRIACAO) com Polling Ativo.
2. **Módulos (20 Sistemas):** Unidades lógicas de processamento (Contexto, Segurança, Auditoria, etc).
3. **Skills:** Interfaces de habilidades funcionais (ex: Execução de Scripts, Skill de Contexto).
4. **Sub-skills:** Unidades técnicas atômicas (ex: Sanitização de comandos, Validação de sintaxe).

---

## 🛠️ BACKLOG DE DESENVOLVIMENTO (FASES)

### [FASE 0] PREPARAÇÃO E LIMPEZA (GREENFIELD)
- [x] **[INFRA] Limpeza Local:** Deleção total do diretório antigo em `/opt/AERIS`.
- [x] **[DBA] Reset de Dados:** Deleção da base MySQL aeris_db e usuários antigos (MySQL 8.0).
- [x] **[INFRA] Purga de Repositório:** Deleção do repositório GitHub antigo para reset de histórico e segredos.
- [x] **[INFRA] Novo Repositório:** Recriação do repositório eugeniosofiati/AERIS no GitHub.
- [x] **[INFRA] Segurança Git:** Configuração de autenticação via PAT (Personal Access Token).
- [x] **[INFRA] Primeiro Commit:** STATUS.md versionado e enviado ao GitHub (Branch: master).

### [FASE 1] INFRAESTRUTURA & CORE (O Esqueleto)
- [x] **[INFRA] Estrutura Física:** Criação dos diretórios `src/`, `config/`, `data/`, `logs/` e `tests/` em `/opt/AERIS`.
- [x] **[INFRA] Dockerização (Base):** Criação do `Dockerfile` (Python 3.11-slim) e `requirements.txt`.
- [x] **[INFRA] Orquestração Docker:** `docker-compose.yml` configurado com `extra_hosts` (host-gateway) para comunicação com MySQL local no Host.
- [x] **[INFRA] Build da Imagem:** Execução do `docker compose build` e geração da imagem `aeris-aeris-app`.
- [x] **[DEV] Fix de Importação Python:** Injeção de `PYTHONPATH=/app` no Dockerfile para permitir imports modulares.
- [x] **[DEV] Shutdown Gracioso:** Implementação de `signal.signal` (SIGTERM/SIGINT) para encerramento limpo (Eliminação do erro 137).
- [x] **[DEV] Orquestrador Modular Base:** Implementação da classe `OrchestratorAeris` com loop controlado por sinais.
- [x] **[DEV] Gestão de Estados:** Polling Ativo implementado no loop principal, permitindo Hot-Swap reativo via banco de dados.
- [ ] **[INFRA] Setup Docker Multi-Network:**
    - Criar aeris_internal (Isolada): Auditoria, Logs.
    - Criar aeris_bridge (Exposta): Orquestrador.
- [ ] **[QA] Teste de Stress de Inicialização:** Validar se todos os módulos sobem em estado BASE.

### [FASE 2] BANCO DE DADOS & PERSISTÊNCIA (O Sistema Nervoso)
- [x] **[DBA] Conectividade Host-Container:** Homologação de conexão via `host.docker.internal:3306` com sucesso (Teste 'SELECT 1').
- [x] **[DBA] Modelagem Relacional AERIS:**
    - [x] Tabela `usuarios_autorizados` (Matriz de Autoridade criada).
    - [x] Tabela `auditoria_imutavel` (Estrutura de logs imutáveis criada).
    - [x] Inserção de Autoridade Suprema: Usuário `geninho` (ID 0) como MESTRE.
    - [x] Ajuste de Resiliência: Remoção de restrição de FK para permitir registro de usuários não autorizados.
    - [x] Tabela `contexto_profundo` (Memória de Longo Prazo/Mestre criada).
    - [x] Tabela `contexto_superficial` (Memória de Curto Prazo/Volátil criada).
- [x] **[DEV] Skill de Contexto:** Métodos `ler_contexto` e `salvar_contexto` integrados ao Orquestrador para persistência dinâmica.
- [ ] **[DEV] Camada de Persistência:** Implementar CRUD com criptografia AES-256 para dados sensíveis do Mestre.
- [ ] **[QA] Teste de Isolamento de Dados:** Garantir que queries de "Visitante" nunca acessem tabelas de "Contexto Profundo".

### [FASE 3] O AGENTE & PIPELINE DE EXECUÇÃO (O Cérebro)
- [x] **[DEV] Skill de Execução & Sub-skill de Sanitização:** Restauração dos arquivos e integração com o Orquestrador.
- [x] **[DEV] Gatekeeper de Identificação:** Migração da lógica de ID 0 hardcoded para consulta dinâmica no Banco de Dados (Finalizado).
- [x] **[DEV] Auditoria Automatizada:** Implementação do registro automático de cada comando na tabela `auditoria_imutavel`.
- [x] **[QA] Teste de Validação Zero Trust:** Homologação do bloqueio de IDs inexistentes (ID 99) e sucesso do ID 0 (Mestre).
- [ ] **[DEV] Pipeline de 10 Etapas (Completo):** Integração total dos estados e módulos.

### [FASE 4] MELHORIAS, TELEMETRIA & MEED (Evolução)
- [ ] **[DEV] Sistema de Telemetria:** Monitoramento de uso de CPU/Memória sem captura de conteúdo.
- [ ] **[DEV] Módulo MEED (Evolução):** Motor de sugestão de novas skills baseado em falhas de fallback.
- [ ] **[QA] Teste de Reversibilidade:** Simular falha crítica e validar o Rollback de estado para BASE.

---

## 🔐 MATRIZ DE ACESSO E CONECTIVIDADE (MINUCIOSA)

### 1. Usuário Mestre (Authority - ID 0)
* **Permissões:** Acesso ROOT ao ecossistema. Pode alterar código-fonte via estado CRIACAO.
* **Memória:** Acesso ao Contexto Profundo e Persistente (Long-term memory).
* **Visibilidade:** Recebe logs técnicos completos e raciocínio de "cadeia de pensamento" (Chain of Thought).
* **Comunicação:** Interface direta com o Orquestrador via canal seguro.

### 2. Usuário Visitante (Guest - ID > 0)
* **Permissões:** Restritas a consultas de leitura e comandos pré-aprovados na Whitelist.
* **Memória:** Acesso apenas ao Contexto Superficial e Volátil (apagado após o encerramento da sessão).
* **Isolamento:** Não possui conhecimento da existência do Usuário Mestre ou de módulos de nível profundo.
* **Segurança:** Toda interação é filtrada pela Sub-skill de Sanitização antes de chegar ao Orquestrador.

### 3. Conectividade Externa
* **Entrada:** Gateway único. O Orquestrador é o único componente que "ouve" o mundo externo.
* **Saída:** Bloqueada por padrão. Saídas de dados exigem autorização em tempo real do Mestre ou Skill de saída validada.

---

## 📑 HISTÓRICO DE ENTREGAS E VALIDAÇÕES

### Snapshot 1.3.9 - Estabilização de Ciclo de Vida (18/04/2026)
* **Status:** CONCLUÍDO ✅
* **Ação:** Implementação de Signal Handling no Orquestrador. Resolução do erro 137.

### Snapshot 1.4.0 - Modelagem de Dados e Matriz de Autoridade (18/04/2026)
* **Status:** CONCLUÍDO ✅
* **Ação:** Criação das tabelas `usuarios_autorizados` e `auditoria_imutavel`.

### Snapshot 1.4.1 - Gatekeeper Dinâmico e Auditoria (18/04/2026)
* **Status:** CONCLUÍDO ✅
* **Ação:** Orquestrador integrado ao Banco de Dados. Identificação de atores via SQL e registro automático de logs.

### Snapshot 1.4.2 - Homologação Zero Trust (18/04/2026)
* **Status:** CONCLUÍDO ✅
* **Ação:** Validação técnica do bloqueio de usuários não autorizados (Teste ID 99).

### Snapshot 1.4.3 - Criação da Estrutura de Memória (18/04/2026)
* **Status:** CONCLUÍDO ✅
* **Ação:** Modelagem e criação das tabelas de contexto profundo e superficial.

### Snapshot 1.4.4 - Integração de Estados e Memória (18/04/2026)
* **Status:** CONCLUÍDO ✅
* **Ação:** Implementação simultânea da Skill de Contexto e da Lógica de Estados no Orquestrador.

### Snapshot 1.4.5 - Hot-Swap Ativo e Correção de Boot (18/04/2026)
* **Status:** CONCLUÍDO ✅
* **Ação:** Resolução da redundância de log no boot (consciência imediata). Implementação de Polling Ativo no loop principal, permitindo que o sistema mude de modo instantaneamente ao alterar o banco, sem necessidade de entrada de comandos.

---

## 📝 PRÓXIMA AÇÃO (BACKLOG IMEDIATO)
1. Executar o Teste de Hot-Swap via comando UPDATE SQL e validar resposta automática no log.
2. Iniciar a codificação das 10 etapas do Pipeline no Orquestrador.
