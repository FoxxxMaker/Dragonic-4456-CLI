import time
import sys
from colorama import init, Fore, Style
import Carregar_Modelo as CM
import Checar_Tamanho as CHK
import Chat as CH
from pathlib import Path

#Versão 0.3

def carregar_modelo():
    modelos = Mostrar_Modelos() # mostra os modelos disponíveis para o usuário escolher
    # Carrega o arquivo do modelo
    # pede para o usuário digitar o nome do modelo que deseja carregar
    
    numero_digitado = input("Digite o numero do modelo que deseja carregar:") 

    indice = int(numero_digitado) - 1 # subtrai 1 do número digitado para obter o índice correto da lista de modelos 
    path = modelos[indice]
    
    # Verifica se o caminho existe
    if path.exists():
        return path
    else:
        print("caminho inválido, tente novamente.")
        # retorna o caminho do modelo para a função checar_tamanho
        return carregar_modelo()

   
def checar_tamanho(path):
    # chama a função checar_tamanho do arquivo Checar_Tamanho.py,
    # e retorna o resultado para a função carregar_modelo
    return CHK.checar_tamanho(path) 


def Mostrar_Modelos():
    # Define o caminho da pasta para PathLib
    pasta = Path('Models')
    modelos = sorted(pasta.glob("*.gguf")) # Lista todos os arquivos com a extensão .gguf na pasta Models
    
    n = 0
    print("Modelos disponíveis:")
    for arquivo, n in enumerate(pasta.iterdir(), start=1):
        n += 0 
        print(f"[{n}] - {arquivo.name}")
    return modelos

# Logotipo em forma de dragão

init()

logo = [
    (Fore.LIGHTCYAN_EX, "   ______________________      /\\"),
    (Fore.CYAN,         "            ________          \\/"),
    (Fore.LIGHTBLUE_EX, "            ______            /\\"),
    (Fore.BLUE,         "   _____________________)")
]

for cor, linha in logo:
    print(cor + linha)

print(Style.RESET_ALL)

print("=" * 30)
print("Dragonic 4456 Console V0.1")

#Começo do Menu principal
print(" ")

print("Olá! Bem vindo ao Dragonic 4456!")
print("Por favor, aguarde")

print(" ")


for i in range(21):
    barra = "#" * i + " " * (20 - i)
    porcentagem = i * 5
    sys.stdout.write(f"\r[{barra}] {porcentagem}%")
    sys.stdout.flush()
    time.sleep(0.15)


print("\nSistema pronto!")

enter = input("Pressione ENTER para começar ou qualquer coisa para sair")

if enter == "":
    path = carregar_modelo()
    
    if checar_tamanho(path):
        modelo = CM.carregar_modelo(path)
        CH.chat(modelo)
    else:
        print("saindo....")
        sys.exit()