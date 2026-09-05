# Diário de execução

Registro interno de trabalho da equipe: decisões técnicas, resultados inesperados, falsos positivos descartados, dificuldades e pendências. Este arquivo é material de apoio, atualizado livremente ao longo do projeto; o conteúdo relevante é reescrito em linguagem acadêmica ao alimentar `relatorio/relatorio.md`, mas o diário em si não é entregue como parte do relatório.

Cada entrada deve trazer data, autor e um resumo objetivo do que foi feito ou decidido.

## Entradas

### 2026-09-05 — Fases 2, 3 e 4: Docker dos dois cenários e validação de isolamento

**Feito:** `docker-compose.yml` e `.env.example` criados para Juice Shop (`bkimminich/juice-shop:v20.2.0`) e WebGoat/WebWolf (`webgoat/webgoat:v2025.3`), ambas as tags escolhidas por serem a versão de release estável mais recente disponível no Docker Hub no momento da configuração (consultado via API do Docker Hub e página de releases do GitHub de cada projeto), evitando `latest`. Digests registrados nos READMEs de cada cenário. Os dois ambientes subiram, ficaram `healthy` e foram validados com recriação completa (`down` + `up`), retornando ao mesmo estado. Isolamento validado: as três portas de host (3000, 8081, 9090) escutam exclusivamente em `127.0.0.1` (confirmado no host com `Get-NetTCPConnection`, não apenas pela configuração do Compose); uma tentativa de conexão do contêiner do WebGoat ao IP interno do contêiner do Juice Shop não obteve resposta em 6 segundos, consistente com ausência de rota entre as redes `labnet-js` e `labnet-wg`.

**Erros e obstáculos:**
- A porta 8080 sugerida pelo roteiro do trabalho para o WebGoat já estava em uso, nesta máquina, por um container de outro projeto (`protected-areas-sc-airflow-webserver`). Resolvido mapeando o host para 8081, mantendo a porta interna do container em 8080; documentado em `docker/webgoat/.env.example` e no README.
- A imagem do Juice Shop (`bkimminich/juice-shop`) é distroless: não tem `/bin/sh`, apenas o binário do Node. Um healthcheck com `CMD-SHELL` não funcionaria; foi necessário usar a forma `CMD` (array, sem shell) chamando `/nodejs/bin/node -e "..."` diretamente.
- No Git Bash (Windows), `--entrypoint /nodejs/bin/node` era convertido automaticamente para um caminho Windows (`C:/Program Files/Git/nodejs/bin/node`) pela conversão de path do MSYS, quebrando o teste manual do binário. Contornado com `MSYS_NO_PATHCONV=1` na frente do comando. Isso não afeta o `docker-compose.yml` em si (o healthcheck roda dentro do container, sem passar pelo MSYS), apenas os comandos manuais de investigação rodados direto no terminal.
- O teste de alcançabilidade entre os dois contêineres (via `wget` do WebGoat até o Juice Shop) não respeitou o timeout `-T` do `wget` do BusyBox na fase de conexão e ficou pendurado; precisou ser refeito envolvendo o comando com `timeout 6 ...` do lado de fora para obter um resultado determinístico (o próprio hang, interrompido de forma controlada, já era a evidência de ausência de rota).

**Handoff para a Fase 5 (preparação do ambiente de ferramentas):** os dois alvos estão de pé e acessíveis (`http://127.0.0.1:3000` e `http://127.0.0.1:8081/WebGoat` + `http://127.0.0.1:9090/WebWolf`), então já é possível apontar ZAP, Burp e sqlmap contra eles para o teste de conectividade da Fase 5. Falta: criar o ambiente virtual Python e `scripts/common/*.py` (ainda são só READMEs de intenção); nenhuma ferramenta de apoio (ZAP, Burp, sqlmap, Nikto) foi instalada ou configurada ainda.

**Evidência coletada 100% por linha de comando (Claude):** digests de imagem, status de saúde dos containers, sub-redes e gateways (`docker network inspect`), confirmação de bind em loopback (`Get-NetTCPConnection`), teste de não alcançabilidade entre redes, HTTP 200 nas páginas de login de cada alvo.

**Evidência que depende do usuário (fora do alcance de linha de comando neste ambiente):** nenhuma nesta fase. Nenhuma captura de tela ou interação de navegador foi necessária para validar infraestrutura; isso muda a partir da Fase 6/7 (reconhecimento) e principalmente da Fase 9/10 (investigação OWASP), quando screenshots de DevTools, uso interativo do Burp Repeater e do ZAP em modo proxy exigem participação direta do usuário, porque não há navegador nem interface gráfica acessível por este terminal.
