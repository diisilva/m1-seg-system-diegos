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

Validado com `docker network inspect`, `docker port` e, no host, `Get-NetTCPConnection` (Windows):

| Cenário | Rede Docker | Sub-rede | Gateway | Endereço do alvo |
|---|---|---|---|---|
| Juice Shop | `labnet-js` | `172.24.0.0/16` | `172.24.0.1` | `http://127.0.0.1:3000` |
| WebGoat | `labnet-wg` | `172.25.0.0/16` | `172.25.0.1` | `http://127.0.0.1:8081/WebGoat` |
| WebWolf | `labnet-wg` | `172.25.0.0/16` | `172.25.0.1` | `http://127.0.0.1:9090/WebWolf` |

## Evidência de isolamento coletada

- **Bind exclusivo em loopback:** `Get-NetTCPConnection -LocalPort 3000,8081,9090 -State Listen` no host mostra as três portas escutando apenas em `127.0.0.1`, nunca em `0.0.0.0`. `docker port` confirma o mesmo mapeamento (`3000/tcp -> 127.0.0.1:3000`, `8080/tcp -> 127.0.0.1:8081`, `9090/tcp -> 127.0.0.1:9090`).
- **Sem rota entre as duas redes:** a partir do container `labnet-wg-webgoat` (rede `labnet-wg`), uma tentativa de conexão HTTP ao IP interno do container `labnet-js-juice-shop` (rede `labnet-js`, `172.24.0.2:3000`) não completa: nem sucesso nem recusa de conexão, apenas timeout (testado com um limite de 6 segundos, sem resposta). Esse comportamento é consistente com a ausência de rota entre as duas redes bridge, que não compartilham rede nem estão conectadas uma à outra. O teste no sentido inverso (Juice Shop tentando alcançar o WebGoat) não foi possível de forma automatizada porque a imagem do Juice Shop não possui shell (imagem distroless, apenas o binário do Node); a garantia de isolamento nesse sentido decorre da mesma configuração de rede, simétrica por padrão no Docker.
- **Recriação determinística:** os dois ambientes foram derrubados (`docker compose down`) e recriados (`docker compose up -d`) a partir do zero, retornando ao mesmo estado saudável (`healthy`) e às mesmas portas, sem qualquer configuração manual adicional.
