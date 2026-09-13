"""Trava de escopo para os scripts de investigação.

Garante que nenhuma requisição disparada pelos scripts deste projeto
alcance um host fora do alvo local autorizado, reproduzindo em código a
restrição de que toda exploração deste trabalho ocorre exclusivamente
contra o laboratório controlado pela própria equipe, em `127.0.0.1`.
"""

from __future__ import annotations

from urllib.parse import urlsplit

from scripts.lib import config


class OutOfScopeError(RuntimeError):
    """Levantada quando uma URL de destino está fora do escopo autorizado."""


def assert_in_scope(url: str) -> None:
    """Garante que `url` aponta para o host e a porta autorizados.

    Args:
        url: URL de destino da requisição prestes a ser enviada.

    Raises:
        OutOfScopeError: quando o host ou a porta de `url` não pertencem ao
            escopo local autorizado.
    """
    parts = urlsplit(url)
    host = parts.hostname
    default_port = 443 if parts.scheme == "https" else 80
    port = parts.port or default_port

    if host not in config.ALLOWED_HOSTS:
        raise OutOfScopeError(
            f"Host fora de escopo: {host!r}. Permitidos: {config.ALLOWED_HOSTS}."
        )
    if port not in config.ALLOWED_PORTS:
        raise OutOfScopeError(
            f"Porta fora de escopo: {port!r}. Permitidas: {config.ALLOWED_PORTS}."
        )
