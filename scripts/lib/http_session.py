"""Sessão HTTP com trava de escopo e registro automático de evidência.

Envolve `requests.Session` para que todo script de investigação use o
mesmo caminho de código para enviar requisições: a URL é sempre validada
contra o escopo autorizado antes do envio, e a evidência, quando um
gravador é fornecido, é sempre registrada no mesmo formato.
"""

from __future__ import annotations

from typing import Any

import requests

from scripts.lib.evidence import EvidenceRecorder
from scripts.lib.scope_guard import assert_in_scope


class ScopedSession:
    """Sessão HTTP restrita ao escopo do alvo, com evidência opcional."""

    def __init__(self, recorder: EvidenceRecorder | None = None) -> None:
        """Inicializa a sessão.

        Args:
            recorder: gravador de evidência opcional; quando fornecido,
                toda requisição concluída é registrada automaticamente,
                independentemente do status HTTP retornado (inclui
                respostas de erro, como as tentativas incorretas de
                V6 e V7).
        """
        self._session = requests.Session()
        self._recorder = recorder

    def request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        """Envia uma requisição HTTP dentro do escopo autorizado.

        Args:
            method: verbo HTTP (`GET`, `POST`, ...).
            url: URL completa de destino; deve pertencer ao escopo autorizado.
            **kwargs: demais argumentos aceitos por `requests.Session.request`.

        Returns:
            A resposta HTTP obtida.

        Raises:
            scripts.lib.scope_guard.OutOfScopeError: quando `url` não
                pertence ao escopo autorizado.
        """
        assert_in_scope(url)
        response = self._session.request(method, url, **kwargs)
        if self._recorder is not None:
            self._recorder.record(response)
        return response

    def get(self, url: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs: Any) -> requests.Response:
        return self.request("POST", url, **kwargs)

    def close(self) -> None:
        self._session.close()
