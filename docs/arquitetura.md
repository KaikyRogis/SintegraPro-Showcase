# Arquitetura

## Visão de alto nível

O SintegraPro é organizado em quatro blocos principais:

- **Core**: motor de processamento SINTEGRA
- **Client**: aplicativo desktop Electron usado em produção
- **Installer Bootstrapper**: shell visual de setup, update e uninstall
- **Server de suporte**: API auxiliar para cenários externos e compatibilidade

## Papéis de máquina

### Servidor

- API local do produto
- PostgreSQL local
- publicação manual de updates
- backup e restauração
- operação local com shell desktop

### Estação

- processamento local
- sincronização com servidor
- consumo de updates publicados
- operação orientada pelo host/IP da API do servidor

## Princípios técnicos

- processamento fiscal sempre local
- persistência principal em PostgreSQL
- atualização distribuída pela rede local
- fluxos críticos com interface guiada
- separação entre runtime do produto e materiais de apresentação
