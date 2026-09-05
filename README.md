# Avaliação de vulnerabilidades: OWASP Juice Shop e OWASP WebGoat

Trabalho de Segurança de Sistemas Computacionais, com avaliação de vulnerabilidades em duas aplicações web deliberadamente vulneráveis, executadas localmente em Docker: OWASP Juice Shop e OWASP WebGoat. Os dois cenários são investigados de forma independente e comparados ao final; a estrutura do repositório mantém tudo o que pertence a cada cenário separado, sem misturar configuração, scripts ou evidências entre eles.

## Objetivo

Instanciar os dois alvos em contêiner Docker, identificar e classificar vulnerabilidades segundo o OWASP Top 10:2021 e o CWE, pontuar a severidade com CVSS e relacionar cada achado à tríade Confidencialidade/Integridade/Disponibilidade e às implicações de privacidade sob a LGPD.

## Escopo

Toda exploração ocorre exclusivamente contra os alvos vulneráveis executados localmente por este repositório, acessíveis apenas em `127.0.0.1`. Nenhum teste é realizado contra sistemas de terceiros, IPs públicos ou serviços fora deste laboratório.

## Aviso de uso

Os alvos deste repositório são propositalmente vulneráveis e destinam-se exclusivamente a este trabalho acadêmico, em ambiente local e isolado. A reprodução deste material contra qualquer sistema não autorizado pelo próprio operador é ilegal (Lei nº 12.737/2012) e está fora do escopo deste projeto.

## Estrutura do projeto

Cada cenário tem sua própria configuração Docker, seus próprios scripts e sua própria pasta de evidências e achados, para que fique claro a qualquer momento a qual cenário cada arquivo pertence:

```
docker/juiceshop/      configuração Docker exclusiva do Juice Shop
docker/webgoat/        configuração Docker exclusiva do WebGoat
scripts/common/        módulos Python reutilizados pelos dois cenários (sessão HTTP, evidência, escopo)
scripts/juiceshop/     provas de conceito específicas do Juice Shop
scripts/webgoat/       provas de conceito específicas do WebGoat
achados/juiceshop/     registro de achados confirmados no Juice Shop
achados/webgoat/       registro de achados confirmados no WebGoat
evidencias/juiceshop/  evidências brutas coletadas no Juice Shop
evidencias/webgoat/    evidências brutas coletadas no WebGoat
comparacao/            matriz comparativa entre os dois cenários
docs/                  metodologia, convenção de evidências e isolamento de rede
relatorio/             relatório técnico da entrega, em Markdown e PDF
```

## Requisitos

- Docker e Docker Compose (plugin `compose`) funcionais.
- Python 3.11 ou superior, para os scripts em `scripts/`.
- Opcional para a investigação: navegador com DevTools, OWASP ZAP, Burp Suite Community, sqlmap, Nikto.

## Arquitetura

Dois laboratórios independentes, cada um em sua própria rede Docker bridge, sem rota entre si e sem publicação de porta fora de `127.0.0.1`. Detalhes em `docs/isolamento-rede.md`.

## Preparação

Nenhuma instalação adicional é necessária além do Docker para subir os alvos. Para a investigação com scripts Python, crie um ambiente virtual e instale as dependências:

```
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

## Execução

Cada cenário sobe e desce de forma independente, com seu próprio `docker-compose.yml`.

### Juice Shop

```
docker compose -f docker/juiceshop/docker-compose.yml up -d
docker compose -f docker/juiceshop/docker-compose.yml down
```

Acesso: `http://127.0.0.1:3000`. Porta de host configurável em `docker/juiceshop/.env` (veja `.env.example`).

### WebGoat

```
docker compose -f docker/webgoat/docker-compose.yml up -d
docker compose -f docker/webgoat/docker-compose.yml down
```

Acesso: `http://127.0.0.1:8081/WebGoat` (WebGoat) e `http://127.0.0.1:9090/WebWolf` (WebWolf). A porta do WebGoat é 8081, não a 8080 sugerida pelo roteiro do trabalho, por conflito com outro serviço local; veja `docker/webgoat/README.md`. Portas configuráveis em `docker/webgoat/.env` (veja `.env.example`). Na primeira execução, o WebGoat pede a criação de um usuário local, exclusivo deste ambiente.

## Scripts disponíveis

_A preencher conforme os scripts de `scripts/` forem implementados e consolidados._

## Coleta de evidências

_A preencher com um resumo da convenção descrita em `docs/convencao-evidencias.md`._

## Limpeza

_A preencher com os comandos de `docker compose down` e remoção de recursos de cada cenário._

## Troubleshooting

**Porta de host já em uso.** Se `docker compose up` falhar por porta ocupada, verifique o que já está escutando nela (`Get-NetTCPConnection -LocalPort <porta>` no Windows, `ss -ltn` no Linux/macOS) e crie um `.env` no diretório do cenário correspondente (a partir do `.env.example`), definindo uma porta livre. Não é necessário editar o `docker-compose.yml`. Nesta configuração, a porta do WebGoat já foi ajustada de 8080 para 8081 por esse motivo.

**WebGoat demora a ficar saudável.** É uma aplicação Java/Spring; o healthcheck usa `start_period` de 45 segundos e várias tentativas antes de reportar falha. Acompanhe com `docker compose -f docker/webgoat/docker-compose.yml ps`.

## Limitações

_A preencher ao final da investigação, com o que não foi coberto ou não pôde ser confirmado._
