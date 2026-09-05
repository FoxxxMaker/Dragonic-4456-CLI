# 🐉 Dragonic 4456 Console — V0.1

## Visão geral

A V0.1 marcou a primeira versão funcional do Dragonic 4456 Console: um
protótipo de IA local em Python para carregar modelos `.gguf` e conversar pelo
terminal.

O foco desta versão foi estabelecer o fluxo básico do programa e separar suas
responsabilidades em arquivos simples.

## Recursos incluídos

- Inicialização do programa por CLI.
- Logo e tela de boas-vindas no terminal.
- Listagem de arquivos da pasta `Models/`.
- Escolha manual do modelo a carregar.
- Verificação de existência e tamanho do arquivo.
- Carregamento de modelos por `llama-cpp-python`.
- Chat básico de pergunta e resposta.
- Organização inicial em `Main.py`, `Chat.py`, `Carregar_Modelo.py` e
  `Checar_Tamanho.py`.

## Como usar

1. Instale as dependências do projeto.
2. Coloque um arquivo `.gguf` em `Models/`.
3. Rode `python Main.py`.
4. Escolha um dos modelos mostrados no terminal.
5. Digite uma mensagem para receber uma resposta do modelo.

## Melhorias introduzidas nesta primeira etapa

- O projeto deixou de ser apenas uma ideia de CLI e passou a carregar um modelo
  local de verdade.
- O código foi dividido em módulos, facilitando futuras alterações.
- A checagem de tamanho passou a impedir o carregamento de arquivos acima do
  limite definido pelo projeto.

## Limitações conhecidas

- Não havia configuração externa para prompt ou parâmetros de geração.
- O chat ainda não oferecia um comando próprio para sair.
- A seleção do arquivo exigia digitar o nome do modelo.

> Para os avanços seguintes, veja [V0.2](README-v0.2.md) e
> [V0.3](README-v0.3.md).
