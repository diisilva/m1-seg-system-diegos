# Convenção de coleta e organização de evidências

## Estrutura de diretórios

```
evidencias/<cenario>/<achado-id>-<slug>/
├── contexto.md                 metadados da coleta
├── screenshots/
│   └── NN-descricao-curta.png
├── http/
│   ├── NN-request-descricao.http
│   └── NN-response-descricao.http
├── ferramentas/
│   └── NN-ferramenta-saida.txt
└── sistema/
    └── NN-docker-logs.txt
```

- `<cenario>`: `juiceshop` ou `webgoat`.
- `<achado-id>`: `V-JS-01`, `V-JS-02`, ... para Juice Shop; `V-WG-01`, `V-WG-02`, ... para WebGoat. Atribuído assim que a hipótese vira achado candidato, não apenas quando confirmada; achados descartados mantêm a pasta, com nota de descarte em `contexto.md`, para rastreabilidade.
- `<slug>`: descrição curta em kebab-case (ex.: `idor-cesta`, `sqli-login`).
- `NN`: prefixo sequencial de dois dígitos, na ordem em que a evidência foi coletada.

## O que registrar por tipo de evidência

| Evidência | O que deve conter | Onde obter |
|---|---|---|
| Screenshot | Tela ou recorte que mostre a URL/contexto, a ação executada e o resultado anômalo visível, nunca um recorte tão fechado que perca o contexto. | Navegador, DevTools (Network, Application, Console), Burp Repeater, ZAP. |
| Requisição (`.http`) | Método, URL completa, cabeçalhos relevantes (`Cookie`, `Authorization`, `Content-Type`), corpo/payload exato. | DevTools Network, Burp Repeater, saída automática dos scripts Python. |
| Resposta (`.http`) | Status HTTP, cabeçalhos relevantes (`Set-Cookie`, cabeçalhos de segurança ausentes), corpo relevante. | DevTools Network, Burp Repeater, scripts Python. |
| Saída de ferramenta | Comando completo executado, versão da ferramenta, saída relevante ao achado. | Terminal (sqlmap, Nikto), relatório do ZAP, export do Burp. |
| Logs/inspeção de sistema | `docker logs`/`docker inspect` no momento do teste, quando o achado depende de configuração de infraestrutura. | Terminal, `docker logs`, `docker network inspect`. |
| Trecho de código | Apenas quando obtido licitamente (código-fonte aberto do projeto vulnerável, stack trace vazado). | Repositório público do projeto, resposta HTTP. |
| Versão de componente | Nome, versão exata e onde foi obtida. | Manifesto do projeto, cabeçalho HTTP, tela "About". |

## Roteiro mínimo de captura por achado

1. Abrir DevTools na aba Network, com "Preserve log" ativo, antes de executar a ação.
2. Executar a ação e localizar a linha correspondente na aba Network.
3. Capturar screenshot mostrando URL, método, status e corpo relevante da resposta.
4. Salvar a requisição bruta em `http/NN-request-*.http`.
5. Salvar a resposta relevante em `http/NN-response-*.http`.
6. Quando uma ferramenta de apoio confirmar ou aprofundar o achado, salvar sua saída em `ferramentas/`.
7. Quando o achado depender de configuração de infraestrutura, salvar `docker logs`/`docker inspect` pertinente em `sistema/`.
8. Preencher `contexto.md` imediatamente após a coleta.
9. Só então criar ou atualizar o arquivo em `achados/<cenario>/<achado-id>-<slug>.md`, referenciando os caminhos exatos dos arquivos de evidência.

## Conteúdo mínimo de `contexto.md`

```
Achado: <achado-id> - <titulo curto>
Timestamp: <data e hora local da coleta>
Responsavel: <integrante da equipe>
Ambiente: <cenario>, imagem <nome:tag>, digest <sha256 se coletado>
Ferramenta(s) usada(s): <nome + versao>
Pre-condicoes: <estado necessario antes da acao>
Passos executados: <lista numerada>
Observacao: <o que se esperava versus o que foi observado>
```

## Regras gerais

- Nenhuma evidência de screenshot isolado sem o par requisição/resposta correspondente, salvo nos casos em que a evidência é conceitual por natureza (ex.: ausência de log).
- Dados sensíveis de terceiros reais nunca aparecem nas evidências; apenas dados de teste criados pela própria equipe dentro do laboratório.
- Evidências descartadas (achado não confirmado) são mantidas, não apagadas, com nota de descarte em `contexto.md`.
