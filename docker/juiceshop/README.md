# Docker: Juice Shop

Configuração exclusiva do cenário OWASP Juice Shop. Nada neste diretório é compartilhado com o WebGoat.

- `docker-compose.yml`: definição do serviço, rede dedicada `labnet-js`, bind em `127.0.0.1`.
- `.env.example`: porta de host padrão (`JUICESHOP_HTTP_PORT=3000`). Copie para `.env` (não versionado) apenas se precisar de outra porta nesta máquina.

_Arquivos a criar na configuração do ambiente Docker deste cenário._
