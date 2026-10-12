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

### GPU via Vulkan ou NVIDIA CUDA

Se o `vulkaninfo --summary` listar sua placa, instale o wheel Vulkan oficial sem compilar C++:

```powershell
powershell -ExecutionPolicy Bypass -File .\install_windows.ps1 -Backend Vulkan
```

Em seguida, execute o Dragonic, abra `2. Configurações do sistema`, selecione `10` e informe `-1` para tentar transferir todas as camadas do modelo para a GPU. Use `0` para voltar imediatamente ao modo CPU ou um valor positivo quando a VRAM não suportar o modelo inteiro. O programa impede a inicialização com GPU caso o wheel instalado ainda seja somente CPU.

Para NVIDIA, instale o wheel CUDA oficial. Escolha a versão CUDA que seu driver suporta; `cu121` é o padrão seguro do instalador e as opções disponíveis são `cu118`, `cu121`, `cu122`, `cu123`, `cu124`, `cu125`, `cu130` e `cu132`:

```powershell
powershell -ExecutionPolicy Bypass -File .\install_windows.ps1 -Backend CUDA -CudaVersion cu121
```

Também existe o atalho abaixo: ele prioriza CUDA quando `nvidia-smi` está disponível, tenta Vulkan em seguida e mantém CPU se não detectar nenhum dos dois.

```powershell
powershell -ExecutionPolicy Bypass -File .\install_windows.ps1 -Backend Auto
```

### Solução de problemas

- **`No matching distribution found for llama-cpp-python`**: confira `python --version`, arquitetura de 64 bits e conexão com o índice. Instale Python 3.12 x64, exclua somente a pasta `.venv` e execute o instalador novamente.
- **`DLL load failed`, `ImportError` ou erro de runtime**: instale ou repare o [Microsoft Visual C++ Redistributable x64](https://aka.ms/vs/17/release/vc_redist.x64.exe) e execute o instalador novamente. Isso não equivale a instalar o compilador C++.
- **`CMake Error`, `nmake`, `cl.exe`**: normalmente indicam tentativa de instalação manual a partir do código-fonte. Use o script PowerShell e não apenas `pip install -r requirements.txt`.
- **Ambiente virtual incompatível**: remova `.venv`, nunca `Models/`, e rode o instalador novamente.
- **GPU AMD, NVIDIA ou Vulkan**: para AMD/Intel use `-Backend Vulkan`; para NVIDIA use `-Backend CUDA -CudaVersion cu121`; ou use `-Backend Auto`. Confirme que o script mostra `GPU offload: True` e então escolha as camadas no menu `2` do Dragonic. CUDA pré-compilado requer Python 3.10, 3.11 ou 3.12; se não houver wheel, o script falha sem compilar C++.

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
