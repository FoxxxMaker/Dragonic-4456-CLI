#requires -Version 5.1
<#
Instalacao do Dragonic no Windows x64 usando apenas wheels precompilados.
Evita que o pip tente compilar llama-cpp-python com CMake/MSVC.
Uso: powershell -ExecutionPolicy Bypass -File .\install_windows.ps1
#>
[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$venvDir = Join-Path $PSScriptRoot '.venv'
$venvPython = Join-Path $venvDir 'Scripts\python.exe'
$requirements = Join-Path $PSScriptRoot 'requirements.txt'
$cpuWheelIndex = 'https://abetlen.github.io/llama-cpp-python/whl/cpu'
$checkPython = "import sys, struct; print('Python:', sys.version.split()[0], 'arquitetura:', struct.calcsize('P') * 8, 'bits'); sys.exit(0 if (3, 10) <= sys.version_info[:2] <= (3, 13) and struct.calcsize('P') == 8 else 1)"

if ($env:OS -ne 'Windows_NT') {
    throw 'Este instalador foi feito para Windows. Consulte o README para Linux.'
}

if (-not (Test-Path $venvPython)) {
    if (Get-Command 'py' -ErrorAction SilentlyContinue) {
        $pythonCommand = 'py'
        $pythonArgs = @('-3')
    }
    elseif (Get-Command 'python' -ErrorAction SilentlyContinue) {
        $pythonCommand = 'python'
        $pythonArgs = @()
    }
    else {
        throw 'Python nao encontrado. Instale Python 3.12 x64 e habilite o comando py ou python.'
    }

    & $pythonCommand @pythonArgs -c $checkPython
    if ($LASTEXITCODE -ne 0) {
        throw 'Use Python 3.10 a 3.13 de 64 bits (recomendado: Python 3.12 x64).'
    }

    Write-Host 'Criando ambiente virtual em .venv ...'
    & $pythonCommand @pythonArgs -m venv $venvDir
    if ($LASTEXITCODE -ne 0) {
        throw 'Falha ao criar .venv. Verifique se o modulo venv esta disponivel.'
    }
}

& $venvPython -c $checkPython
if ($LASTEXITCODE -ne 0) {
    throw 'O ambiente .venv existente usa Python incompatível. Remova .venv e execute este script novamente.'
}

Write-Host 'Atualizando pip ...'
& $venvPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    throw 'Falha ao atualizar pip. Verifique a conexao com a internet.'
}

Write-Host 'Instalando wheels de CPU (sem compilar C/C++) ...'
& $venvPython -m pip install --only-binary=:all: --extra-index-url $cpuWheelIndex -r $requirements
if ($LASTEXITCODE -ne 0) {
    throw 'Nenhum wheel compativel ou download falhou. Verifique Python x64, rede e acesso ao indice oficial. O script nao compila C++.'
}

Write-Host 'Verificando dependencias e carregamento da biblioteca nativa ...'
& $venvPython -m pip check
if ($LASTEXITCODE -ne 0) {
    throw 'Dependencias inconsistentes no ambiente virtual.'
}

& $venvPython -c "from llama_cpp import Llama; import colorama; print('OK: llama_cpp e colorama importados')"
if ($LASTEXITCODE -ne 0) {
    throw 'A importacao falhou. Verifique DLLs/Visual C++ Redistributable do Windows; nenhuma compilacao foi realizada.'
}

Write-Host ''
Write-Host 'Instalacao concluida! Para iniciar:'
Write-Host '  .\.venv\Scripts\python.exe Main.py'
