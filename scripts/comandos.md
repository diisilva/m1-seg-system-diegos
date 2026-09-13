# Comandos auxiliares de exploração

Este arquivo documenta comandos manuais de referência para investigação com as ferramentas de apoio. Os comandos que de fato produziram os achados confirmados (V1 a V7) estão registrados em [`../relatorio/tabela-de-achados.md`](../relatorio/tabela-de-achados.md), junto com a requisição e a resposta completas; este arquivo não duplica esse conteúdo, serve como referência rápida de como acionar cada ferramenta.

## sqlmap

Contra o endpoint de login, forma que confirmou V1 (comando completo e saída em `tabela-de-achados.md`):

```bash
sqlmap -u "http://127.0.0.1:3000/rest/user/login" \
  --data='{"email":"test@test.com","password":"test"}' \
  --headers="Content-Type: application/json" \
  -p email --batch --level 3 --risk 2 --ignore-code=401
```

O `--ignore-code=401` é necessário porque o endpoint de login retorna 401 para credenciais inválidas, e o sqlmap trata isso como falha de autenticação por padrão, recusando-se a prosseguir sem esse ajuste.

Outros pontos de entrada do roteiro (busca de produtos, `/rest/products/search?q=1`) podem ser testados da mesma forma, mas não geraram achado confirmado nesta investigação:

```bash
sqlmap -u "http://127.0.0.1:3000/rest/products/search?q=1" --batch
```

## OWASP ZAP

A varredura efetivamente usada (spider e varredura passiva, que sinalizou a ausência de CSP aprofundada em V4) rodou via Docker, sem interface gráfica:

```bash
docker run --rm --network vulnerable-web-application_labnet zaproxy/zap-stable \
  zap-baseline.py -t http://juice-shop:3000
```

Para uma investigação manual mais aprofundada, com Active Scan dirigido e HUD, use a interface gráfica: configure o ZAP como proxy do navegador, rode o Spider contra `http://127.0.0.1:3000` e o Active Scan apenas contra o alvo local, exportando o relatório de alertas para `../evidencias/`. Esse fluxo interativo ainda não foi empregado neste repositório.

## Nikto

Ainda não empregado em nenhum achado confirmado neste repositório. Comando de referência, caso venha a ser usado em investigação futura (A05, A08, A09 ou A10):

```bash
nikto -h http://127.0.0.1:3000
```

## Inspeção manual (DevTools)

Base da evidência original de V1 a V3:

- Aba **Network**: cabeçalhos de resposta, `Set-Cookie` (flags Secure/HttpOnly), tokens.
- Aba **Console/Application**: cookies, localStorage, JWT.
