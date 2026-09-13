"""Gravação padronizada de evidências HTTP em disco.

Cada par de requisição e resposta é salvo em
`evidencias/<achado_id>-<slug>/http/`, complementando os prints e
capturas de tela já existentes com o par requisição/resposta em texto,
necessário para que cada achado seja reproduzível por outra pessoa sem
depender apenas da imagem.
"""

from __future__ import annotations

from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parents[2]


class EvidenceRecorder:
    """Grava sequencialmente pares de requisição/resposta de um achado candidato."""

    def __init__(self, achado_id: str, slug: str) -> None:
        """Inicializa o gravador para um achado específico.

        Args:
            achado_id: identificador do achado (ex.: `V1`).
            slug: descrição curta em kebab-case (ex.: `sqli-login`).
        """
        self._dir = REPO_ROOT / "evidencias" / f"{achado_id}-{slug}" / "http"
        self._dir.mkdir(parents=True, exist_ok=True)
        self._counter = 0

    @property
    def directory(self) -> Path:
        """Diretório `http/` onde os pares de requisição/resposta são gravados."""
        return self._dir

    @property
    def achado_directory(self) -> Path:
        """Diretório do achado, um nível acima de `directory`, para artefatos extras."""
        return self._dir.parent

    def record(self, response: requests.Response) -> Path:
        """Grava a requisição e a resposta associadas a `response`.

        Args:
            response: resposta HTTP já concluída; `response.request` deve
                conter a requisição original preparada pelo `requests`.

        Returns:
            O diretório onde os dois arquivos foram gravados.
        """
        self._counter += 1
        seq = f"{self._counter:02d}"
        self._write(f"{seq}-request.http", self._format_request(response.request))
        self._write(f"{seq}-response.http", self._format_response(response))
        return self._dir

    def _write(self, filename: str, content: str) -> None:
        (self._dir / filename).write_text(content, encoding="utf-8")

    @staticmethod
    def _format_request(request: requests.PreparedRequest) -> str:
        lines = [f"{request.method} {request.url}"]
        lines += [f"{key}: {value}" for key, value in request.headers.items()]
        lines.append("")
        if request.body:
            body = request.body
            if isinstance(body, bytes):
                body = body.decode("utf-8", errors="replace")
            lines.append(body)
        return "\n".join(lines)

    @staticmethod
    def _format_response(response: requests.Response) -> str:
        lines = [f"HTTP {response.status_code} {response.reason}"]
        lines += [f"{key}: {value}" for key, value in response.headers.items()]
        lines.append("")
        lines.append(response.text)
        return "\n".join(lines)
