import os
import rich
import time
import sys
from colorama import init, Fore, Style

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


