# 🐉 Dragonic 4456 Console — V0.3

Dragonic 4456 é um protótipo de chat local em Python. Ele carrega modelos `.gguf` da pasta `Models/` e permite conversar com eles pelo terminal usando `llama-cpp-python`.

> Esta documentação descreve a V0.3. A V0.4 está em desenvolvimento.

## Funcionalidades

- Interface de terminal inspirada em BIOS, com menu de inicialização e status.
- Chat local com histórico em memória e backup automático da sessão em JSON.
- Configuração em `Config.json`.

## Instalação no Windows (recomendada)

Requisitos: **Windows x64 e Python 3.10–3.13 de 64 bits** (recomendado Python 3.12 x64), com acesso à internet.

No PowerShell, dentro da pasta clonada ou extraída do projeto:

```powershell
powershell -ExecutionPolicy Bypass -File .\install_windows.ps1
```

O instalador cria `.venv`, instala a dependência nativa usando **wheels pré-compilados de CPU**, bloqueia builds C++ locais e valida o carregamento de `llama_cpp`. Não é necessário instalar Visual Studio Build Tools para compilar o pacote. Alguns computadores podem precisar do **Microsoft Visual C++ Redistributable x64** para executar as DLLs já compiladas.

Depois, coloque um modelo `.gguf` em `Models/` e execute:

```powershell
.\.venv\Scripts\python.exe Main.py
```

O modo padrão utiliza CPU. A aceleração GPU requer wheels específicos e **não é configurada por este instalador**. Consulte [Instalação](docs/Instalação.md) para diagnóstico de erros.

## Linux / instalação manual

Use Python 3.10–3.13 e um ambiente virtual. Em Linux, instalar `llama-cpp-python` pode exigir ferramentas de compilação C/C++ caso não exista wheel adequado.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python Main.py
```

## Configuração

O arquivo [Config.json](Config.json) reúne:

- `system_prompt`: instruções iniciais do modelo.
- `max_tokens`: máximo de tokens por resposta.
- `temperature`: variação de resposta.
- `stop`: sequências de parada.
- `echo`: se inclui o prompt na saída.
- `historico_max_mensagens`: quantidade máxima de mensagens em memória.
- `backup_chats_habilitado`: ativa ou desativa o backup ao encerrar um chat.
- `diretorio_backup_chats`: pasta local que recebe os arquivos JSON de backup.

Os backups preservam a conversa completa, mesmo quando o limite do histórico de contexto reduz as mensagens enviadas ao modelo. Por privacidade, a pasta `backups_chats/` não é enviada ao Git.

## Documentação

- [Instalação](docs/Instalação.md)
- [Uso](docs/Uso.md)
- [Modelos GGUF](docs/Modelos)
- [Configuração](docs/Configuração.md)
- [Roadmap](docs/roadmap.md)

## Tecnologias e licença

Python, [llama-cpp-python](https://github.com/abetlen/llama-cpp-python), Colorama. Licença [MIT](LICENSE).
