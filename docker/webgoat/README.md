# Docker: WebGoat

Configuração exclusiva do cenário OWASP WebGoat (WebGoat + WebWolf). Nada neste diretório é compartilhado com o Juice Shop.

- `docker-compose.yml`: definição dos serviços, rede dedicada `labnet-wg`, bind em `127.0.0.1`.
- `.env.example`: portas de host padrão (`WEBGOAT_HTTP_PORT=8081`, `WEBWOLF_HTTP_PORT=9090`). A porta do WebGoat é 8081, não 8080, porque 8080 já está em uso nesta máquina por outro projeto sem relação com este trabalho; a porta interna do container continua 8080. Copie para `.env` (não versionado) apenas se precisar de outra porta nesta máquina.

## Imagem

- Tag: `webgoat/webgoat:v2025.3` (última versão com release formal no momento da configuração; o Docker Hub também publica uma tag `2026` de build contínuo a partir da branch principal, descartada aqui por não ser reprodutível da mesma forma que uma tag de release).
- Digest: `sha256:3101bd9e7bcfe122d7ef91e690ef3720de36cc4e86b3d06763a1ddf2e2751a4b`

## Uso

```
docker compose -f docker/webgoat/docker-compose.yml up -d
docker compose -f docker/webgoat/docker-compose.yml ps
docker compose -f docker/webgoat/docker-compose.yml down
```

Acesso: `http://127.0.0.1:8081/WebGoat` (WebGoat) e `http://127.0.0.1:9090/WebWolf` (WebWolf), ou nas portas definidas em `.env`, quando customizadas. A primeira execução pede a criação de um usuário local, exclusivo deste ambiente de laboratório.

