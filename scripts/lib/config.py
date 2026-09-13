"""Configuração de acesso ao alvo.

Lê a porta de host do Juice Shop a partir de `.env` na raiz do repositório
(com fallback para `.env.example` e, por fim, para o valor padrão 3000),
de forma que uma porta customizada localmente se propague automaticamente
para a trava de escopo em `scope_guard.py`.
"""

from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_dotenv(path: Path) -> None:
    """Carrega pares chave=valor de um arquivo `.env` simples no ambiente do processo."""
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


_load_dotenv(REPO_ROOT / ".env")
_load_dotenv(REPO_ROOT / ".env.example")

JUICESHOP_HTTP_PORT = int(os.environ.get("JUICESHOP_HTTP_PORT", "3000"))
BASE_URL = f"http://127.0.0.1:{JUICESHOP_HTTP_PORT}"
ALLOWED_HOSTS = ("127.0.0.1", "localhost")
ALLOWED_PORTS = (JUICESHOP_HTTP_PORT,)
