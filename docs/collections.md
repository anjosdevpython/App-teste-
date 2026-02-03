# Collections do PocketBase

As collections abaixo formam a base do ERP Anjos EduTech. Ajuste regras conforme o perfil de acesso (Admin, Direção, Secretaria, Financeiro, Professor).

## Convenções gerais

- Todos os registros possuem `created`, `updated`, `created_by` e `updated_by` (campos de auditoria).
- Relacionamentos usam `relation` do PocketBase.
- Campos sensíveis (CPF, dados de pagamento) devem ter acesso restrito ao Financeiro e Direção.

## Collections principais

### users (auth)
- Perfis: `admin`, `direcao`, `secretaria`, `financeiro`, `professor`.
- Campos: `name`, `role`, `active`, `last_login`.

### alunos
- Campos: `nome_completo`, `data_nascimento`, `cpf_responsavel`, `endereco`, `contato_responsavel`, `status`.
- Regras: leitura por secretaria/direção; edição restrita.

### turmas
- Campos: `nome`, `ano_letivo`, `turno`, `professor_responsavel` (relation users).

### matriculas
- Campos: `aluno` (relation alunos), `turma` (relation turmas), `data_matricula`, `status`, `bolsa`.

### professores
- Campos: `nome_completo`, `formacao`, `especialidade`, `contato`.

### aulas
- Campos: `turma` (relation), `data`, `conteudo`, `objetivos`, `professor`.

### frequencias
- Campos: `aluno` (relation), `turma` (relation), `data`, `presenca`.

### notas
- Campos: `aluno` (relation), `turma` (relation), `avaliacao`, `nota`, `periodo`.

### pagamentos
- Campos: `aluno` (relation), `competencia`, `valor`, `status`, `forma_pagamento`.

### logs
- Campos: `usuario` (relation users), `acao`, `ip`, `detalhes`, `data_evento`.

## LGPD
- Collection `consentimentos` (opcional): armazena `aluno`, `termo`, `data_consentimento`.
- Exportações devem ser feitas via API ou interface administrativa.
