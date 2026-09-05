# 🐉 Dragonic 4456 Console — V0.2

## Visão geral

A V0.2 refinou o fluxo criado na V0.1. O objetivo foi tornar a seleção e a
verificação de modelos mais organizadas antes de introduzir novas opções de
configuração.

## Novidades em relação à V0.1

- Uso de `pathlib.Path` para trabalhar com a pasta `Models/` e os caminhos dos
  arquivos.
- Listagem de modelos usando a API de caminhos do Python.
- Verificação do tamanho movida para antes da animação de carregamento.
- Saída mais direta quando o modelo não passa na verificação.
- Tela inicial atualizada: `ENTER` inicia o programa e qualquer outro texto
  encerra a execução.
- Redução de poluição visual no chat.

## Fluxo de uso

1. Execute `python Main.py`.
2. Pressione `ENTER` para continuar.
3. Escolha um modelo mostrado em `Models/`.
4. O programa verifica o arquivo antes de iniciar o carregamento.
5. Converse com o modelo pelo terminal.

## Melhorias desta versão

A V0.2 deixou a base mais legível e preparou o projeto para configurações mais
flexíveis. Em especial, `Path` torna o código de arquivos mais claro e facilita
a manutenção futura.

## Limitações conhecidas

- As configurações de geração ainda estavam definidas no código.
- O chat não possuía arquivo próprio de configuração.
- Não existia ainda uma licença adicionada ao repositório.

> Confira a [V0.1](README-v0.1.md) para a base do projeto e a
> [V0.3](README-v0.3.md) para as configurações em JSON.
