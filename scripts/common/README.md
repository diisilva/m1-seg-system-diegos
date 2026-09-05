# scripts/common

Único ponto de reuso entre os dois cenários. Nada específico de Juice Shop ou WebGoat entra aqui.

- `http_session.py`: sessão HTTP (`requests`) com log automático de requisição e resposta.
- `evidence.py`: gravação padronizada de evidências em `evidencias/<cenario>/<achado-id>-<slug>/`.
- `scope_guard.py`: trava de escopo, recusa qualquer requisição fora de `127.0.0.1`/`localhost` nas portas configuradas.
- `config.py`: leitura de configuração por cenário (URL base, portas), a partir dos arquivos `.env` de cada cenário.

_Módulos a implementar na preparação do ambiente de ferramentas._
