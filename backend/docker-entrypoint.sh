#!/usr/bin/env bash
set -euo pipefail

BACKUP_INTERVAL_SECONDS=${BACKUP_INTERVAL_SECONDS:-21600}
BACKUP_DIR=${BACKUP_DIR:-/pb/backups}
DATA_DIR=${DATA_DIR:-/pb/pb_data}

mkdir -p "$BACKUP_DIR" "$DATA_DIR"

echo "[entrypoint] Iniciando PocketBase..."

/pb/pocketbase migrate --dir /pb/pb_migrations || true

backup_loop() {
  while true; do
    timestamp=$(date +%Y%m%d_%H%M%S)
    backup_file="$BACKUP_DIR/pocketbase_backup_${timestamp}.zip"
    echo "[backup] Gerando backup em ${backup_file}"
    /pb/pocketbase backup --dir "$DATA_DIR" --name "$backup_file" || true
    sleep "$BACKUP_INTERVAL_SECONDS"
  done
}

backup_loop &

exec /pb/pocketbase serve --http=0.0.0.0:8090 --dir "$DATA_DIR"
