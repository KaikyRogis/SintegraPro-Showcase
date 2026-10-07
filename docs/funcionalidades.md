# Funcionalidades

## Núcleo operacional

- processamento local de arquivos fiscais
- correção e validação de arquivos SINTEGRA
- SPED Fiscal: conciliação assistida com XML CT-e e geração de TXT separado
- SPED Contribuições (QA controlado): conferência com SPED Fiscal e XML CT-e, regra fiscal ativa, análise de elegibilidade e geração de TXT separado
- XML NF-e/NFC-e de suporte somente quando a análise exigir evidência de produto, NCM ou devolução; exceções documentais impedem correção automática
- validação do TXT gerado no PGE e revisão pelo responsável fiscal antes de qualquer entrega
- preservação de fluxo com backup temporário e validação final

## Operação do produto

- login local com shell desktop
- dashboard operacional
- histórico de execução
- configurações por papel da máquina
- ajuda e diagnóstico do sistema
- limpeza manual ou automática da tela após sucesso, sem apagar o arquivo gerado ou o histórico

## Limites atuais

- o Gestor Fiscal está temporariamente bloqueado
- SPED Contribuições não substitui o arquivo original nesta candidata
- não há transmissão automática da escrituração

## Infraestrutura local

- modo Servidor com PostgreSQL e API local
- modo Estação apontando para o host/IP do servidor
- backup e restauração do ambiente
- instalador, updater e desinstalador visuais

## Distribuição e manutenção

- publicação manual de updater no servidor
- estações consultam updates na rede local
- fluxo de manutenção coordenado por versão alvo e estado do rollout
