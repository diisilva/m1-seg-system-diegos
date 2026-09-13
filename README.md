# Trabalho 1: Avaliação de Vulnerabilidades em Aplicação Web

**Disciplina:** Segurança de Sistemas Computacionais, 2026/2 (UNIVALI)
**Case Prático 1, Módulo M1** · OWASP Top 10:2021 · Docker · CVSS · CWE

Alvo escolhido: **Cenário A, OWASP Juice Shop** (loja online deliberadamente vulnerável, mantida pela OWASP).

> **Ética e legalidade.** O alvo é propositalmente vulnerável e roda em rede isolada,
> acessível apenas em `127.0.0.1`. Testar sistemas de terceiros sem autorização é crime (conforme professor falou em aula)
> (Lei 12.737/2012). Todo teste deste trabalho é feito no próprio ambiente local.

---

## Equipe

| Nome | Papel na execução |
| --- | --- |
| Leonardo Pacheco B Dias | Subida inicial do ambiente Docker; identificação e evidência original dos achados obrigatórios A01, A02 e A03 (V1 a V3); redação do relatório |
| Diego Fonseca da Silva | Reprodutibilidade do ambiente Docker; scripts de prova de conceito de V1 a V7; identificação, evidência e classificação de V4 a V7; validação de CWE e CVSS de todos os achados; estruturação das evidências; redação do relatório |
| Gustavo Gonçalves Trindade | Revisão de código, testes, revisão do relatório e apoio na coleta de evidências das vulnerabilidades |
| João Victor Rodrigues Santos | Revisão de código, testes e revisão do relatório |

---

## Como subir o ambiente

Pré-requisitos: **Docker Desktop** aberto e com o motor rodando ("Engine running").

```bash
docker compose up -d
```

Acesse: **http://127.0.0.1:3000** (ou na porta definida em `.env`, se a 3000 já estiver em uso na sua máquina, copie `.env.example` para `.env` e ajuste `JUICESHOP_HTTP_PORT`, sem editar o `docker-compose.yml`).

Para derrubar:

```bash
docker compose down
```

A imagem é fixada em uma tag versionada (`bkimminich/juice-shop:v20.2.0`, não `latest`), para que o ambiente seja o mesmo em qualquer máquina e em qualquer data. Digest da imagem, para conferência: `sha256:8739101ade29358abb5469ee66ae78e582c97ed0a5543a4ad102e5fa5193526b` (obtido com `docker inspect --format='{{index .RepoDigests 0}}' bkimminich/juice-shop:v20.2.0` após o primeiro `docker compose up`). O contêiner tem healthcheck configurado; `docker compose ps` mostra `healthy` quando o Juice Shop está pronto para uso.

### Endereços de rede a documentar no relatório

- **Alvo:** http://127.0.0.1:3000
- **Rede Docker:** bridge isolada `labnet`, sub-rede `172.19.0.0/16`. Reconfirme a qualquer momento com:
  ```bash
  docker network inspect vulnerable-web-application_labnet
  ```
- **Máquina de teste:** host local (Windows).

---

## Cobertura de vulnerabilidades (mínimo 6 categorias)

Obrigatórias: **A01**, **A02**, **A03**. As demais para fechar 6.

| ID  | OWASP                            | Categoria       | Status       | Achado(s)                                                        |
| --- | --------------------------------- | --------------- | ------------ | ------------------------------------------------------------------ |
| A01 | Broken Access Control            | **obrigatória** | Confirmada   | V3: IDOR na cesta                                                 |
| A02 | Cryptographic Failures           | **obrigatória** | Confirmada   | V2: hash de senha exposto no JWT                                  |
| A03 | Injection (SQLi/XSS)             | **obrigatória** | Confirmada   | V1: SQLi no login, bypass para admin                              |
| A04 | Insecure Design                  | opcional        | Confirmada   | V7: redefinição de senha via pergunta de segurança sem limite de tentativas |
| A05 | Security Misconfiguration        | opcional        | Confirmada   | V4: erro verboso/cabeçalhos; V5: listagem de diretório            |
| A06 | Vulnerable & Outdated Components | opcional        | Investigada  | versão do Express já corrigida; sem achado confirmado             |
| A07 | Identification & Auth Failures   | opcional        | Confirmada   | V6: login sem bloqueio contra força bruta                         |

Cobertura mínima **já atingida**: 6 categorias distintas confirmadas (A01, A02, A03, A04, A05, A07), 7 achados. A08, A09 e A10 ainda não foram investigadas. Detalhes completos, evidência e classificação em [`relatorio/tabela-de-achados.md`](relatorio/tabela-de-achados.md).

> Para categorias não encontradas no alvo, o relatório deve **explicar por que não se aplicam ou não foram observadas**.

---

## Estrutura do repositório

```
.
├── README.md            # este arquivo
├── docker-compose.yml   # ambiente do alvo (Juice Shop), imagem fixa + healthcheck
├── .env.example         # porta de host configuravel (copie para .env se precisar mudar)
├── pyproject.toml       # dependencias dos scripts Python (requests)
├── scripts/
│   ├── comandos.md      # comandos sqlmap/ZAP/Nikto documentados
│   ├── lib/             # sessao HTTP, gravacao de evidencia e trava de escopo, reutilizados pelos PoCs
│   ├── v1_sqli_login.py                     # reproduz V1 (A03)
│   ├── v2_hash_senha_jwt.py                 # reproduz V2 (A02)
│   ├── v3_idor_cesta.py                     # reproduz V3 (A01)
│   ├── v6_bruteforce_login.py               # reproduz V6 (A07)
│   └── v7_reset_senha_pergunta_seguranca.py # reproduz V7 (A04)
├── evidencias/           # prints originais + uma pasta por achado com requisicao/resposta em texto
└── relatorio/            # relatorio tecnico (rascunho + tabela de achados) e fontes
```

### Executando os scripts de prova de conceito

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows; no Linux/macOS: source .venv/bin/activate
pip install -e .
python -m scripts.v1_sqli_login
python -m scripts.v2_hash_senha_jwt
python -m scripts.v3_idor_cesta
python -m scripts.v6_bruteforce_login
python -m scripts.v7_reset_senha_pergunta_seguranca
```

Cada execução grava requisição e resposta em `evidencias/<achado>/http/`. A trava de escopo em `scripts/lib/scope_guard.py` recusa qualquer requisição fora de `127.0.0.1`, mesmo se o script for alterado por engano.

---

## Ferramentas de apoio

Além dos scripts Python, os achados usaram:

- **sqlmap**, via Docker (`googlesky/sqlmap`), para confirmar a injeção booleana cega em V1: `docker run --rm --network vulnerable-web-application_labnet googlesky/sqlmap -u "http://juice-shop:3000/rest/user/login" --data='{"email":"a","password":"b"}' -p email --batch --ignore-code=401`.
- **OWASP ZAP**, via Docker, imagem oficial (`zaproxy/zap-stable`), em modo `zap-baseline.py` (spider e varredura passiva), que sinalizou a ausência de CSP aprofundada em V4.
- **Postman**, para reproduzir manualmente as requisições de V4 e V5 e capturar a resposta renderizada (modo Preview).
- **jwt.io**, para decodificar visualmente o JWT do administrador em V2.
- **Nikto**, ainda não empregado em nenhum achado confirmado.

O uso interativo do ZAP (proxy pelo navegador, Active Scan dirigido) e do Burp Suite Community (Proxy, Repeater) depende de interface gráfica e não foi automatizado.

Os comandos completos de sqlmap, ZAP e Nikto, incluindo o fluxo manual do ZAP via proxy, estão em [`scripts/comandos.md`](scripts/comandos.md); os comandos que de fato confirmaram cada achado estão em [`relatorio/tabela-de-achados.md`](relatorio/tabela-de-achados.md).

## Coleta de evidências

Cada achado tem uma pasta em `evidencias/<achado-id>-<slug>/`, com o par de requisição e resposta em `http/` (gerado pelos scripts ou capturado manualmente via `curl`/Postman) e, quando aplicável, capturas de tela na raiz da pasta do achado. Os cinco prints originais de V1 a V3 (`evidencias/image*.png`) permanecem como estão, sem reorganização, com a explicação de cada um em `evidencias/README.md`.

## Limpeza

```bash
docker compose down        # derruba e remove o container e a rede
docker compose down -v     # idem, removendo tambem volumes, se algum for adicionado no futuro
```

O ambiente não usa volume persistente: recriar o container (`docker compose up -d` novamente) sempre parte do estado inicial da imagem, sem dados de execuções anteriores.

## Troubleshooting

**Porta 3000 já em uso.** Copie `.env.example` para `.env` e defina `JUICESHOP_HTTP_PORT` para uma porta livre; não é necessário editar o `docker-compose.yml`.

**`docker compose ps` não mostra `healthy`.** Aguarde o `start_period` do healthcheck (20 segundos) antes de considerar falha; se persistir, confira `docker compose logs juice-shop`.

**Scripts Python não encontram o pacote `scripts`.** Execute sempre a partir da raiz do repositório, com o ambiente virtual ativado (`pip install -e .` já deixa o pacote instalado em modo editável).

## Limitações

A cobertura mínima de seis categorias foi atingida (A01, A02, A03, A04, A05, A07), mas A08, A09 e A10 ainda não foram investigadas. A categoria A06 foi investigada e não gerou achado, pela versão do Express já estar corrigida contra os CVEs relevantes conhecidos no momento da análise. O uso interativo de ZAP e Burp Suite Community, que dependem de interface gráfica, não foi empregado além do que está descrito na seção de ferramentas.

---

## Entregas

- **Entrega 1 (AVA) até 05/09/2026:** relatório PDF + scripts + este repositório Git.
- **Entrega 2 (seminário, em aula) 14/09/2026:** slides + demonstração ao vivo.
