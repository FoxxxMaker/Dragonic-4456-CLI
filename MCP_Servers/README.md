# Integrações MCP externas

O Dragonic guarda neste diretório o cadastro local de servidores MCP em `servidores.json`.

Use o menu **MCP e integrações** para registrar um servidor por comando e argumentos. Exemplo para uma integração Node:

```text
Nome: meu-servidor
Comando: npx
Argumentos: -y|nome-do-pacote-mcp
```

O arquivo `servidores.json` é local e não vai para o Git, porque pode conter caminhos específicos da máquina. Nesta etapa, o Dragonic prepara e gerencia o cadastro `stdio`; a conexão e a chamada das ferramentas desses servidores será a próxima camada do cliente MCP.
