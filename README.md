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

_A preencher: versões de Docker, Docker Compose e Python usadas pela equipe._

## Arquitetura

_A preencher com o diagrama de rede e a descrição de isolamento entre os dois laboratórios._

## Preparação

_A preencher com os passos de instalação das ferramentas de apoio (Docker, ambiente virtual Python, ZAP, Burp Community, sqlmap, Nikto)._

## Execução

_A preencher com os comandos gerais de subida e derrubada dos ambientes._

### Juice Shop

_A preencher com o comando `docker compose` específico, a porta de acesso e o endereço final._

### WebGoat

_A preencher com o comando `docker compose` específico, as portas de acesso (WebGoat e WebWolf) e o endereço final._

## Scripts disponíveis

_A preencher conforme os scripts de `scripts/` forem implementados e consolidados._

## Coleta de evidências

_A preencher com um resumo da convenção descrita em `docs/convencao-evidencias.md`._

## Limpeza

_A preencher com os comandos de `docker compose down` e remoção de recursos de cada cenário._

## Troubleshooting

_A preencher com problemas comuns observados durante a execução (ex.: conflito de porta de host, já tratado via `.env.example` de cada cenário)._

## Limitações

_A preencher ao final da investigação, com o que não foi coberto ou não pôde ser confirmado._
