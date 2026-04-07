# SintegraPro Showcase

SintegraPro é um sistema desktop desenvolvido para processamento, correção e validação de arquivos fiscais, com foco em confiabilidade operacional, produtividade interna e experiência guiada para ambientes em modo Servidor e Estação.

Este repositório contém apenas a vitrine técnica e visual do projeto.
O código-fonte completo, regras de negócio, integrações, artefatos operacionais e fluxos internos permanecem em repositório privado.

## O que este repositório mostra

- visão geral do produto
- funcionalidades principais
- arquitetura em alto nível
- fluxo das telas
- stack tecnológica
- materiais visuais de apresentação

## Visão geral

O produto foi desenhado para operação Windows em rede local, com dois papéis de máquina:

- **Servidor**: hospeda API local, PostgreSQL, backup, restore e publicação de updates
- **Estação**: processa arquivos localmente, sincroniza histórico com o servidor e recebe updates publicados

## Principais capacidades

- processamento local de arquivos SINTEGRA
- correção e validação assistida
- histórico operacional
- configuração guiada por papel da máquina
- backup e restauração
- update distribuído em rede local
- instalador, updater e desinstalador visuais

## Estrutura deste repositório

```text
SintegraPro-Showcase/
├─ README.md
├─ assets/
│  ├─ imagens/
│  ├─ gifs/
│  └─ video-demo/
├─ docs/
│  ├─ arquitetura.md
│  ├─ funcionalidades.md
│  ├─ fluxo-de-telas.md
│  └─ stack-tecnologica.md
└─ mock/
   └─ layout-estatico/
```

## Documentação

- [Arquitetura](./docs/arquitetura.md)
- [Funcionalidades](./docs/funcionalidades.md)
- [Fluxo de telas](./docs/fluxo-de-telas.md)
- [Stack tecnológica](./docs/stack-tecnologica.md)

## Materiais visuais

Use estas pastas para publicar a apresentação visual do projeto:

- `assets/imagens/`
- `assets/gifs/`
- `assets/video-demo/`
- `mock/layout-estatico/`

## Segurança e escopo

Este repositório **não** inclui:

- código-fonte completo
- integrações internas
- regras de negócio detalhadas
- banco de dados e migrations reais
- instaladores operacionais
- credenciais, chaves, tokens ou configurações sensíveis

## Status

- produto em evolução contínua
- repositório público com foco em apresentação técnica e portfólio
- implementação real mantida em repositório privado
