# Docker: WebGoat

Configuração exclusiva do cenário OWASP WebGoat (WebGoat + WebWolf). Nada neste diretório é compartilhado com o Juice Shop.

- `docker-compose.yml`: definição dos serviços, rede dedicada `labnet-wg`, bind em `127.0.0.1`.
- `.env.example`: portas de host padrão (`WEBGOAT_HTTP_PORT=8081`, `WEBWOLF_HTTP_PORT=9090`). A porta do WebGoat é 8081, não 8080, porque 8080 já está em uso nesta máquina por outro projeto sem relação com este trabalho; a porta interna do container continua 8080. Copie para `.env` (não versionado) apenas se precisar de outra porta nesta máquina.

_Arquivos a criar na configuração do ambiente Docker deste cenário._
