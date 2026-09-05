# Isolamento de rede

## Controles adotados

1. **Bind exclusivo em loopback.** Todo mapeamento de porta usa `127.0.0.1:<porta-host>:<porta-container>`, nunca publicando em `0.0.0.0`.
2. **Rede Docker dedicada por cenário.** `labnet-js` (Juice Shop) e `labnet-wg` (WebGoat/WebWolf), cada uma criada implicitamente pelo respectivo `docker-compose.yml`, sem rede compartilhada entre os dois cenários e sem `network_mode: host`.
3. **Trava de escopo em código.** `scripts/common/scope_guard.py` recusa qualquer requisição cujo destino não seja `127.0.0.1`/`localhost` nas portas configuradas para o cenário ativo, lidas de `scripts/common/config.py`.
4. **Ferramentas apontadas apenas ao alvo local.** OWASP ZAP, Burp Suite Community e sqlmap são configurados com escopo restrito à URL local do cenário em investigação.
5. **Sem exposição residual.** Ao final de cada sessão de trabalho, os containers são derrubados (`docker compose down`).
6. **Enquadramento legal.** Nenhum teste deste repositório mira sistema de terceiros; a Lei nº 12.737/2012 é citada explicitamente no README como limite de conduta.

## Portas de host

As portas padrão sugeridas pelo roteiro do trabalho podem conflitar com outros serviços já em uso na máquina de cada integrante. Por isso, cada cenário lê a porta de host de um arquivo `.env` local (não versionado), com um `.env.example` versionado definindo o valor padrão adotado pela equipe:

| Cenário | Serviço | Porta de host (padrão) | Porta interna do container |
|---|---|---|---|
| Juice Shop | aplicação | 3000 | 3000 |
| WebGoat | WebGoat | 8081 | 8080 |
| WebGoat | WebWolf | 9090 | 9090 |

A porta de host do WebGoat foi definida em 8081, em vez dos 8080 sugeridos pelo roteiro, porque a porta 8080 já está em uso, em pelo menos uma máquina da equipe, por outro serviço sem relação com este trabalho. A porta interna do container permanece 8080, portanto a aplicação não é afetada; apenas o endereço externo usado para acessá-la muda. Qualquer integrante com conflito de porta diferente cria seu próprio `docker/<cenario>/.env` a partir do `.env.example` correspondente, sem precisar alterar o `docker-compose.yml`.

## Endereços de rede documentados

A preencher, durante a validação de isolamento, com a saída real de `docker network inspect` de cada rede (sub-rede, gateway) e a confirmação de que nenhuma porta responde fora de `127.0.0.1`.

| Cenário | Rede Docker | Sub-rede | Endereço do alvo |
|---|---|---|---|
| Juice Shop | `labnet-js` | _a preencher_ | `http://127.0.0.1:3000` |
| WebGoat | `labnet-wg` | _a preencher_ | `http://127.0.0.1:8081/WebGoat` |
| WebWolf | `labnet-wg` | _a preencher_ | `http://127.0.0.1:9090` |
