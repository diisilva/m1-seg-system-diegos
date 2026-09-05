# Metodologia de investigação

## Ciclo aplicado a cada vulnerabilidade

Cada hipótese de vulnerabilidade, em cada cenário, passa pelo mesmo ciclo:

1. Subir o alvo correspondente em Docker.
2. Explorar manualmente, com apoio de ferramenta quando aplicável.
3. Classificar o achado em OWASP Top 10:2021 e CWE.
4. Pontuar a severidade em CVSS.
5. Relacionar o achado à tríade Confidencialidade/Integridade/Disponibilidade e às implicações de LGPD.
6. Registrar evidência reproduzível.

## Estágios da investigação por categoria

Para cada categoria OWASP investigada em cada cenário:

1. **Exploração manual guiada por hipótese**, com navegador, DevTools e, quando aplicável, Burp Repeater. Este estágio é obrigatório mesmo quando existe automação disponível, porque o comportamento observado é a evidência mais direta de impacto real.
2. **Apoio de ferramenta especializada** (OWASP ZAP, sqlmap, Nikto), quando a categoria se beneficia de varredura ou automação de payloads. A ferramenta orienta a investigação; não substitui a confirmação manual.
3. **Registro do achado**, somente após confirmação, no formato padronizado (`achados/_template.md`), com evidências organizadas conforme `convencao-evidencias.md`.

Categorias que não produzirem achado confirmado após esse ciclo completo são documentadas como não observadas ou não aplicáveis no cenário, com justificativa técnica, nunca omitidas.

## Ordem de investigação

Em cada cenário, as categorias obrigatórias (A01 Broken Access Control, A02 Cryptographic Failures, A03 Injection) são investigadas primeiro. As demais seguem a ordem de maior probabilidade de achado documentada para aquele cenário específico.

## Critério de confirmação de achado

Um achado é considerado confirmado quando o comportamento anômalo é reproduzido de forma determinística, com requisição e resposta que demonstram o desvio em relação ao comportamento esperado da aplicação, revisado por mais de um integrante da equipe.

## Diferenciação de falsos positivos

Nenhum alerta de scanner automático (ZAP, Nikto, sqlmap) é promovido a achado sem confirmação manual, com requisição e resposta próprias da equipe. Um alerta que não se confirma manualmente é descartado e documentado como falso positivo, não como achado.

Um comportamento observado uma única vez, que não se repete seguindo os mesmos passos em nova tentativa, é tratado como não reproduzível e não entra na tabela final de achados confirmados.

## Padrão de classificação

- **OWASP Top 10:2021**: referência de categoria para todo achado.
- **CWE**: todo achado confirmado tem seu CWE validado na base oficial do MITRE (`cwe.mitre.org`) antes de ser considerado final; nenhum CWE é assumido apenas pela categoria OWASP.
- **CVSS**: versão 3.1, com vetor completo, score, severidade e justificativa por métrica, validado na calculadora oficial do FIRST (`first.org/cvss/calculator/3.1`).
- **CID e LGPD**: analisados separadamente para cada achado, nunca tratados como sinônimos.
