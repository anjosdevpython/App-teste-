# Anjos EduTech ERP

Sistema ERP educacional para o **É Tempo de Crescer – Centro Educacional**, com execução local via Docker e backend PocketBase.

## ✅ Visão geral

- **Frontend**: React (Vite)
- **Backend**: PocketBase (API + autenticação + banco)
- **Modo**: Local-first / on-premise
- **Persistência**: Docker volumes
- **Backup automático**: PocketBase backup em volume dedicado

## Estrutura de pastas

```
.
├── backend
│   ├── Dockerfile
│   ├── docker-entrypoint.sh
│   └── pb_migrations
├── frontend
│   ├── Dockerfile
│   ├── nginx.conf
│   └── src
├── docs
│   └── collections.md
├── seed
│   ├── README.md
│   └── sample_data.json
└── docker-compose.yml
```

## Como executar (Docker)

```bash
docker compose up --build
```

### Acessos iniciais

- Frontend: `http://localhost:5173`
- PocketBase Admin: `http://localhost:8090/_/`

### Criação do admin

1. Acesse `http://localhost:8090/_/`
2. Crie o primeiro usuário administrador
3. Configure perfis e regras conforme `docs/collections.md`

## Collections documentadas

Consulte `docs/collections.md` para modelagem de dados, regras de acesso e campos sugeridos.

## Dados de exemplo (seed)

- Arquivo: `seed/sample_data.json`
- Instruções: `seed/README.md`

## Backup automático

O backend gera backups em `/pb/backups` a cada 6 horas (configurável via `BACKUP_INTERVAL_SECONDS`).

## Segurança e LGPD

- Controle de acesso por perfil
- Registro de consentimentos
- Logs de acesso e auditoria
- Exportação de dados conforme necessidade

## Diferenciais

- Branding configurável
- Preparado para multiescola
- API pronta para integrações futuras
- Interface responsiva (desktop e tablet)

## Observações

Este projeto é um **monolito modular desacoplado** com foco em simplicidade operacional e evolução contínua.

---

## RecoverX (recuperação de dados)

Este repositório também inclui o **RecoverX**, utilitário local (CLI + GUI Tkinter) para análise forense e recuperação de arquivos via assinatura binária.

- Entrada: dispositivos físicos (quando permitido) e imagens `.img/.dd/.raw`
- Saída: diretório dedicado, com cálculo de hash SHA-256
- Relatórios: JSON em `reports/recovery_report.json`

Documentação completa: `docs/recovery_tool.md`.
