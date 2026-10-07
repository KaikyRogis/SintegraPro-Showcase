# Fluxo de telas

## Fluxo principal

1. Login do usuário
2. Dashboard inicial
3. Processamento de arquivo SINTEGRA
4. SPED Fiscal: selecionar TXT e XML CT-e, processar e validar o arquivo de saída
5. SPED Contribuições (QA): selecionar Contribuições, Fiscal e XML CT-e; analisar; fornecer NF-e/NFC-e se houver bloqueio documental; analisar de novo; gerar TXT; validar no PGE
6. Visualização de histórico
7. Configurações da máquina, inclusive reset após sucesso
8. Backup, restore, update e diagnóstico conforme o papel

## Fluxos auxiliares

- setup inicial em modo Servidor ou Estação
- escolha entre implantação nova e restauração de backup
- publicação manual de updater no servidor
- bloqueio orientado de estação durante manutenção
- desinstalação visual com modos padrão e remoção total local
