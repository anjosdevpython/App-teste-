# RecoverX - Recuperação de Dados (Forense)

## Visão técnica

O RecoverX foi estruturado para trabalhar em **modo somente leitura**, priorizando boas práticas forenses:

- A origem é aberta apenas com `rb` e nunca com flags de escrita.
- O destino deve ser um diretório diferente (definido via CLI/GUI).
- Nenhum conteúdo da mídia é executado; o processo é estritamente binário.

## Arquitetura

```text
core/
  disk_reader.py   -> enumeração de dispositivos e leitura em blocos
  fs_analyzer.py   -> heurísticas NTFS/FAT/exFAT/EXT4 e quick format
  file_carver.py   -> assinatura binária, carving multi-thread e hash
signatures/
  signatures.json  -> catálogo editável de assinaturas
ui/
  cli.py           -> fluxo principal e geração de relatório
  gui.py           -> interface opcional em Tkinter
utils/
  hashing.py
  logger.py
  path_safety.py
  report.py
main.py
```

## Decisões de engenharia

1. **Leitura em blocos (1 MiB por padrão)** para reduzir memória e melhorar throughput.
2. **Carving por assinatura em paralelo** com `ThreadPoolExecutor`, mantendo escrita sincronizada por arquivo.
3. **Heurísticas de fragmentação parcial**: quando footer não é encontrado dentro do limite, o arquivo é salvo como parcial.
4. **Rastreabilidade** por log (`reports/recovery.log`) e relatório JSON (`reports/recovery_report.json`) com hashes SHA-256.
5. **Assinaturas customizáveis** via `signatures/signatures.json`, sem alteração de código.

## Execução

### CLI

```bash
python3 main.py list
python3 main.py scan --source /caminho/origem.img --destination ./output
python3 main.py scan --source /caminho/origem.dd --destination ./output --deep --workers 8
```

### GUI

```bash
python3 main.py --gui
```

## Limitações reais

- Em casos de **criptografia por ransomware**, o RecoverX recupera blocos/arquivos, mas **não descriptografa** dados.
- Em mídias com sobrescrita intensa, a recuperação pode ser parcial ou impossível.
- Parsing avançado de MFT/inodes está em modo heurístico (não substitui suites forenses proprietárias/laboratoriais).
- Acesso a discos físicos pode exigir privilégios administrativos/root.

## Aviso ético e legal

Use somente com autorização formal do proprietário da mídia e respeite legislação local.
Para uso pericial, preserve cadeia de custódia (hash inicial, imagem forense e registro de ações).
