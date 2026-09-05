# Relatório técnico: avaliação de vulnerabilidades em aplicação web

_Documento alimentado incrementalmente ao longo do projeto. Cada seção é preenchida assim que a fase correspondente da investigação produz o conteúdo, não apenas ao final._

## 1. Sumário executivo

_A preencher._

## 2. Passo a passo da configuração do ambiente

Os dois alvos são executados em contêineres Docker independentes, cada um com sua própria rede bridge e definido em um `docker-compose.yml` próprio, sem configuração compartilhada entre os cenários.

**Juice Shop**

```
docker compose -f docker/juiceshop/docker-compose.yml up -d
```

Imagem: `bkimminich/juice-shop:v20.2.0` (digest `sha256:8739101ade29358abb5469ee66ae78e582c97ed0a5543a4ad102e5fa5193526b`). Porta de host: 3000, mapeada para a porta 3000 do contêiner, publicada apenas em `127.0.0.1`. Acesso: `http://127.0.0.1:3000`.

**WebGoat e WebWolf**

```
docker compose -f docker/webgoat/docker-compose.yml up -d
```

Imagem: `webgoat/webgoat:v2025.3` (digest `sha256:3101bd9e7bcfe122d7ef91e690ef3720de36cc4e86b3d06763a1ddf2e2751a4b`). Porta de host do WebGoat: 8081, mapeada para a porta interna 8080 do contêiner. A porta padrão sugerida para o WebGoat (8080) não foi usada porque já está ocupada, na máquina de desenvolvimento da equipe, por outro serviço sem relação com este trabalho; como o mapeamento de porta é apenas o lado externo da publicação Docker, a aplicação em si roda de forma idêntica, apenas acessada por um endereço de host diferente. Porta de host do WebWolf: 9090, mapeada para a porta interna 9090 do contêiner, sem conflito. Acesso: `http://127.0.0.1:8081/WebGoat` e `http://127.0.0.1:9090/WebWolf`.

Ambas as portas de host são parametrizáveis por variável de ambiente (`docker/<cenario>/.env.example`), para que um conflito de porta equivalente, em outra máquina da equipe, não exija alterar o `docker-compose.yml`.

Os dois ambientes foram validados com recriação completa (`docker compose down` seguido de `docker compose up -d`), retornando ao mesmo estado íntegro em ambos os casos, o que confirma a reprodutibilidade da configuração.

## 3. Papel de cada membro da equipe

_A preencher._

## 4. Arquitetura da solução de laboratório

_A preencher._

## 5. Endereços de rede utilizados

Cada cenário roda em sua própria rede Docker do tipo bridge, sem rota entre as duas:

| Cenário | Rede Docker | Sub-rede | Gateway | Endereço do alvo |
|---|---|---|---|---|
| Juice Shop | `labnet-js` | `172.24.0.0/16` | `172.24.0.1` | `http://127.0.0.1:3000` |
| WebGoat | `labnet-wg` | `172.25.0.0/16` | `172.25.0.1` | `http://127.0.0.1:8081/WebGoat` |
| WebWolf | `labnet-wg` | `172.25.0.0/16` | `172.25.0.1` | `http://127.0.0.1:9090/WebWolf` |

O isolamento foi validado de duas formas. No host, a listagem de sockets em escuta (`Get-NetTCPConnection`) confirma que as três portas (3000, 8081, 9090) respondem exclusivamente em `127.0.0.1`, nunca em `0.0.0.0`, portanto inacessíveis a partir de outro dispositivo da rede local. Entre os dois laboratórios, uma tentativa de conexão HTTP do contêiner do WebGoat ao endereço interno do contêiner do Juice Shop (`172.24.0.2:3000`) não obteve resposta dentro de um limite de seis segundos, nem sucesso nem recusa explícita, comportamento consistente com a ausência de rota entre as redes `labnet-js` e `labnet-wg`.

A máquina de teste é o próprio host de desenvolvimento, sem uso de máquina virtual dedicada para este laboratório.

## 6. Ferramentas de apoio utilizadas

_A preencher._

## 7. Explicação dos achados

_A preencher, um achado por vez, conforme confirmado._

### 7.1 Categorias não observadas ou não aplicáveis

_A preencher._

## 8. Conclusão

_A preencher._

## 9. Referências

_A preencher._

## Apêndice: comparação Juice Shop x WebGoat

_A preencher a partir de `comparacao/matriz-comparativa.md`._
