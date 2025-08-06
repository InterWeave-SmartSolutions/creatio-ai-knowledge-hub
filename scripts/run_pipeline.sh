#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." &>/dev/null && pwd)"
LOG_DIR="$ROOT_DIR/logs/pipeline"
OUT_DIR="$ROOT_DIR/out"
mkdir -p "$LOG_DIR" "$OUT_DIR"
TS="$(date -u +%Y%m%d_%H%M%S)"
LOG="$LOG_DIR/$TS.run.log"

echo "[INFO] Starting pipeline at $TS" | tee -a "$LOG"
echo "[INFO] Using config: $ROOT_DIR/config.yaml" | tee -a "$LOG"

# Example steps (idempotent; skip if outputs exist)
# Idempotence guards: skip steps if outputs present
set -x
[ -d "$OUT_DIR/academy_docs" ] || python3 "$ROOT_DIR/academy_docs_scraper.py" --config "$ROOT_DIR/config.yaml" --out "$OUT_DIR/academy_docs" 2>&1 | tee -a "$LOG" || true
[ -d "$OUT_DIR/structure" ] || python3 "$ROOT_DIR/analyze_creatio_structure.py" --config "$ROOT_DIR/config.yaml" --in "$OUT_DIR/academy_docs" --out "$OUT_DIR/structure" 2>&1 | tee -a "$LOG" || true
[ -d "$OUT_DIR/solutions" ] || python3 "$ROOT_DIR/comprehensive_solutions_scraper.py" --config "$ROOT_DIR/config.yaml" --out "$OUT_DIR/solutions" 2>&1 | tee -a "$LOG" || true
set +x

echo "[INFO] Pipeline complete" | tee -a "$LOG"
