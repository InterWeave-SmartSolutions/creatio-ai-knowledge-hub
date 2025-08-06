SHELL := /bin/bash

.PHONY: help audit fm pipeline lint format test clean

help:
@echo "Targets:"
@echo "  audit     - Generate inventory snapshots and markdown audit"
@echo "  fm        - Bulk add front-matter to Markdown (docs, documentation)"
@echo "  pipeline  - Run reproducible data pipeline"
@echo "  lint      - Run linters (eslint/prettier/flake8/black if available)"
@echo "  format    - Format code and docs"
@echo "  test      - Run tests"
@echo "  clean     - Remove generated outputs (out/, logs/pipeline)"

audit:
@bash -lc 'mkdir -p logs/inventory; ts=$$(date -u +%Y%m%d_%H%M%S); prefix=logs/inventory/$$ts; { echo "# Top-level listing"; ls -la; } | tee "$$prefix.ls.txt"; { echo "# Tree overview (depth 2)"; tree -a -L 2 -I ".git|node_modules|.venv|venv|__pycache__|.cache|dist|build|.next|.DS_Store" || true; } | tee "$$prefix.tree.txt"; { echo "# Largest directories"; du -h --max-depth=1 | sort -h; } | tee "$$prefix.du.txt"; { echo "# ripgrep Creatio"; rg -n --no-ignore --hidden -S "Creatio" || true; } | tee "$$prefix.rg_creatio.txt"; { echo "# Filetype counts"; find . -type f -print0 | xargs -0 -I{} sh -c 'f="{}"; ext="$${f##*.}"; echo "$$ext"' | sort | uniq -c | sort -nr; } | tee "$$prefix.filetypes.txt";'
