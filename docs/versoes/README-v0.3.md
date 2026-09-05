# 🐉 Dragonic 4456 Console — V0.3

## Visão geral

A V0.3 tornou o Dragonic mais personalizável. A principal mudança foi retirar
as opções de geração do código e concentrá-las em `Config.json`, para que a
experiência do modelo possa ser ajustada sem editar Python.

## Novidades em relação à V0.2

- Adição do arquivo `Config.json`.
- Prompt de sistema configurável.
- Configuração de `max_tokens`, `temperature`, `stop` e `echo`.
- Comandos `sair`, `exit` e `quit` no chat.
- Contexto do modelo ampliado para 2048 tokens.
- Ocultação dos logs detalhados de carregamento para uma interface mais limpa.
- Adição da licença MIT.
- Documentação de instalação, uso, modelos e configuração.
- Arquivo `requirements.txt` incluído no projeto.

## Configurando o modelo

Edite [Config.json](../../Config.json) antes de abrir o programa:

```json
{
  "system_prompt": "System: Você é uma assistente útil.",
  "max_tokens": 80,
  "temperature": 0.2,
  "stop": ["Usuário:", "\n\n"],
  "echo": false
}
```

O arquivo permite adaptar o tom e o tamanho das respostas sem mexer no código
fonte. Para detalhes de cada opção, veja a página de
[configuração](../Configuração.md).

## Como usar

1. Instale as dependências com `pip install -r requirements.txt`.
2. Coloque um modelo `.gguf` em `Models/`.
3. Execute `python Main.py`.
4. Selecione o modelo e converse pelo terminal.
5. Para encerrar o chat, digite `sair`, `exit` ou `quit`.

## Melhorias desta versão

A V0.3 separou a configuração do comportamento da IA da lógica do programa.
Isso facilita testar personalidades, respostas curtas ou criativas e diferentes
critérios de parada sem alterar arquivos Python.

> A documentação principal da versão está no [README do projeto](../../README.md).
> Compare também com [V0.1](README-v0.1.md) e [V0.2](README-v0.2.md).
