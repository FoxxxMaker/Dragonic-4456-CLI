# 🐉 Dragonic 4456 Console — V0.3

Dragonic 4456 é um protótipo de chat local em Python. Ele carrega modelos
`.gguf` da pasta `Models/` e permite conversar com eles pelo terminal usando
`llama-cpp-python`.

> Esta documentação descreve a V0.3. A V0.4 está em desenvolvimento.

## O que a V0.3 oferece

- Interface de linha de comando com logo e inicialização visual.
- Listagem de modelos disponíveis em `Models/`.
- Escolha e verificação do arquivo antes do carregamento.
- Limite de tamanho para o modelo e animação de carregamento.
- Chat local pelo terminal.
- Comandos `sair`, `exit` e `quit` para encerrar o chat.
- Configuração do comportamento do modelo em `Config.json`.

## Começando

1. Instale as dependências:

   ```powershell
   pip install -r requirements.txt
   ```

2. Coloque um modelo `.gguf` na pasta `Models/`.
3. Execute o programa:

   ```powershell
   python Main.py
   ```

4. Pressione `ENTER`, digite o nome do modelo listado e comece a conversar.

## Configuração

O arquivo [Config.json](Config.json) reúne as opções usadas no chat:

- `system_prompt`: instruções e personalidade inicial do modelo.
- `max_tokens`: quantidade máxima de tokens gerados por resposta.
- `temperature`: grau de variação/criatividade da resposta.
- `stop`: textos que interrompem a geração.
- `echo`: define se o prompt também aparece na saída.

Veja uma explicação mais detalhada em [Configuração](docs/Configuração.md).

## Estrutura

```text
Dragonic-4456-CLI/
├── Main.py
├── Chat.py
├── Carregar_Modelo.py
├── Checar_Tamanho.py
├── Config.json
├── requirements.txt
├── Models/
└── docs/
```

## Documentação

- [Instalação](docs/Instalação.md)
- [Uso](docs/Uso.md)
- [Modelos GGUF](docs/Modelos)
- [Configuração](docs/Configuração.md)
- [Roadmap](docs/roadmap.md)

## Histórico de versões

- [README da V0.1](docs/versoes/README-v0.1.md)
- [README da V0.2](docs/versoes/README-v0.2.md)
- [README da V0.3](docs/versoes/README-v0.3.md)

## Tecnologias

- Python
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
- Colorama

## Licença

Este projeto é distribuído sob a [licença MIT](LICENSE).
