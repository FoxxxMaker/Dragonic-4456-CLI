# Instalação do Dragonic 4456

## Windows x64 — sem compilação C++

1. Instale **Python 3.12 de 64 bits** (também aceita 3.10–3.13).
2. Abra o PowerShell na raiz deste projeto (pasta que contém `Main.py`).
3. Execute:

   ```powershell
   powershell -ExecutionPolicy Bypass -File .\install_windows.ps1
   ```

4. Coloque seu modelo `.gguf` na pasta `Models/`.
5. Inicie:

   ```powershell
   .\.venv\Scripts\python.exe Main.py
   ```

O script usa `pip --only-binary=:all:` e o [índice de wheels de CPU do llama-cpp-python](https://abetlen.github.io/llama-cpp-python/whl/cpu). Se não houver wheel para seu Python/Windows, a instalação **falha de forma explícita**, sem tentar baixar o código e compilar com CMake/MSVC.

### Solução de problemas

- **`No matching distribution found for llama-cpp-python`**: confira `python --version`, arquitetura de 64 bits e conexão com o índice. Instale Python 3.12 x64, exclua somente a pasta `.venv` e execute o instalador novamente.
- **`DLL load failed`, `ImportError` ou erro de runtime**: instale ou repare o [Microsoft Visual C++ Redistributable x64](https://aka.ms/vs/17/release/vc_redist.x64.exe) e execute o instalador novamente. Isso não equivale a instalar o compilador C++.
- **`CMake Error`, `nmake`, `cl.exe`**: normalmente indicam tentativa de instalação manual a partir do código-fonte. Use o script PowerShell e não apenas `pip install -r requirements.txt`.
- **Ambiente virtual incompatível**: remova `.venv`, nunca `Models/`, e rode o instalador novamente.
- **GPU AMD, NVIDIA ou Vulkan**: este instalador instala a versão CPU por padrão; aceleração de GPU exige instalação e testes separados.

## Linux

```bash
git clone https://github.com/FoxxxMaker/Dragonic-4456-CLI
cd Dragonic-4456-CLI
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python Main.py
```

Em Linux, o pip ainda poderá precisar de CMake e de um compilador C/C++ quando não houver wheel adequado.

## Instalação a partir de ZIP

Baixe o ZIP do GitHub, extraia, abra um terminal na pasta extraída e siga os passos Windows ou Linux acima.
