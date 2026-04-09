# Dragonic 4456 Console V0.1

Dragonic 4456 é um sistema protótipo de chat local em Python para carregamento de modelos `.gguf` e interação via terminal.
O projeto foi desenvolvido com foco em simplicidade, organização modular e evolução gradual. Nesta primeira versão, o sistema lista os modelos disponíveis, 
valida o arquivo escolhido, verifica o tamanho antes do carregamento e inicializa um chat em CLI usando `llama-cpp-python`.

## Funcionalidades atuais
- Interface simples em terminal
- Listagem de modelos disponíveis na pasta `Models`
- Validação do caminho do arquivo escolhido
- Verificação de tamanho do modelo antes do carregamento
- Carregamento de modelos `.gguf`
- Chat básico no terminal com entrada e resposta

## Estrutura do projeto

```bash
Dragonic-4456/
├── Main.py
├── Carregar_Modelo.py
├── Checar_Tamanho.py
├── Chat.py
├── requirements.txt
└── Models/
```

# Como funciona🤔

O fluxo atual do programa é:
- Exibir uma tela inicial no terminal
- Mostrar os modelos disponíveis
- Permitir que o usuário escolha um modelo
- Verificar se o arquivo existe
- Checar se o tamanho do modelo está dentro do limite definido
- Carregar o modelo .gguf
- Iniciar o chat no terminal

Como o programa é só um protótipo, é aceito apenas modelos .GGUF menores que 1B que tenham até `900Mb`.

# Tecnologias utilizadas:⚙
- Python
- llama-cpp-python
- colorama

# Requisitos:

Antes de executar o projeto, você precisa ter:

- Python instalado
- Um ambiente virtual configurado
- As dependências instaladas
- Um modelo .gguf (até 900Mb) dentro da pasta Models

## Instalação📌

Clone o repositório:
```
git clone https://github.com/FoxxxMaker/Dragonic-4456-CLI.git
cd CLI
```
Crie e ative um ambiente virtual:

# Windows
```
python -m venv .venv
.venv\Scripts\activate
```
#Instale as dependências:
```
pip install -r requirements.txt
```

# Como executar

Com o ambiente virtual ativado, rode:

```
python Main.py
```
Depois disso:

pressione ENTER para iniciar
escolha um modelo listado na pasta Models
aguarde o carregamento
converse com o modelo pelo terminal
