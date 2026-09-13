"""Prova de conceito de ausência de proteção contra força bruta (A07).

Registra uma conta de teste e envia uma sequência de tentativas de login
com senha incorreta, sem qualquer atraso entre elas. Em seguida, tenta o
login com a senha correta imediatamente após a sequência. A ausência de
bloqueio, CAPTCHA ou atraso crescente, combinada com o sucesso do login
correto logo depois, confirma a falha.
"""

from __future__ import annotations

import uuid

from scripts.lib import config
from scripts.lib.evidence import EvidenceRecorder
from scripts.lib.http_session import ScopedSession

ACHADO_ID = "V6"
SLUG = "bruteforce-login"

TENTATIVAS_SENHA_ERRADA = 15


def executar() -> None:
    """Executa a prova de conceito de ponta a ponta e imprime o veredito."""
    recorder = EvidenceRecorder(ACHADO_ID, SLUG)
    sessao = ScopedSession(recorder=recorder)

    email = f"bruteforce-{uuid.uuid4().hex[:10]}@lab.local"
    senha_correta = "SenhaCorreta#9"

    sessao.post(
        f"{config.BASE_URL}/api/Users",
        json={
            "email": email,
            "password": senha_correta,
            "passwordRepeat": senha_correta,
            "securityQuestion": {"id": 1},
            "securityAnswer": "resposta-de-teste",
        },
    )

    status_tentativas = []
    for indice in range(1, TENTATIVAS_SENHA_ERRADA + 1):
        resposta = sessao.post(
            f"{config.BASE_URL}/rest/user/login",
            json={"email": email, "password": f"senhaErrada{indice}"},
        )
        status_tentativas.append(resposta.status_code)

    resposta_final = sessao.post(
        f"{config.BASE_URL}/rest/user/login",
        json={"email": email, "password": senha_correta},
    )

    bloqueios = [s for s in status_tentativas if s in (403, 429)]
    print(f"Status das {TENTATIVAS_SENHA_ERRADA} tentativas com senha errada: {status_tentativas}")
    print(f"Login com senha correta logo em seguida: HTTP {resposta_final.status_code}")
    if not bloqueios and resposta_final.status_code == 200:
        print(
            "RESULTADO: ausência de proteção contra força bruta confirmada "
            "— nenhuma tentativa foi bloqueada e o login correto teve sucesso "
            "imediatamente depois."
        )
    else:
        print("RESULTADO: alguma forma de bloqueio foi observada, achado não confirmado.")
    print(f"Evidência gravada em: {recorder.directory}")


if __name__ == "__main__":
    executar()
