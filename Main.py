import os
import rich
import time
import sys
from colorama import init, Fore, Style
import Carregar_Modelo as CM
import Checar_Tamanho as CHK


def carregar_modelo():
    Mostrar_Modelos() # mostra os modelos disponíveis para o usuário escolher
    
    # Carrega o arquivo do modelo
    path = input("Digite o caminho do modelo que deseja carregar: ")
    
    # Verifica se o caminho existe
    if os.path.exists(path):
        checar_tamanho()
    else:
        print("caminho inválido, tente novamente.")
        carregar_modelo
    return path # retorna o caminho do modelo para a função checar_tamanho

   
def checar_tamanho():
    path = carregar_modelo() # chama a função carregar_modelo para obter o caminho do modelo

    if CHK.checar_tamanho(path):
        print("Modelo pronto.")
    else:
        print("Modelo grande demais. Tente um menor que 900Mb.")


def Mostrar_Modelos():
    pasta = "Models"
    arquivos = os.listdir(pasta)
    print("Modelos disponíveis:")
    for arquivo in arquivos:
        print(f"- {arquivo}")

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

enter = input("Pressione ENTER para começar")

if enter == "":
    carregar_modelo()