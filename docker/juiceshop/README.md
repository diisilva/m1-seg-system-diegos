# Docker: Juice Shop

Configuração exclusiva do cenário OWASP Juice Shop. Nada neste diretório é compartilhado com o WebGoat.

- `docker-compose.yml`: definição do serviço, rede dedicada `labnet-js`, bind em `127.0.0.1`.
- `.env.example`: porta de host padrão (`JUICESHOP_HTTP_PORT=3000`). Copie para `.env` (não versionado) apenas se precisar de outra porta nesta máquina.

## Imagem

- Tag: `bkimminich/juice-shop:v20.2.0` (versão estável mais recente disponível no Docker Hub no momento da configuração, evitando `latest` por reprodutibilidade).
- Digest: `sha256:8739101ade29358abb5469ee66ae78e582c97ed0a5543a4ad102e5fa5193526b`

## Uso

```
docker compose -f docker/juiceshop/docker-compose.yml up -d
docker compose -f docker/juiceshop/docker-compose.yml ps
docker compose -f docker/juiceshop/docker-compose.yml down
```

Acesso: `http://127.0.0.1:3000` (ou na porta definida em `.env`, quando customizada).

