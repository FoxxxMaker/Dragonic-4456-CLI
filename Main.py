import sys
import time
from pathlib import Path

from colorama import Fore, Style, init

import Carregar_Modelo as CM
import Chat as CH
import Checar_Tamanho as CHK


DIRETORIO_MODELOS = Path(__file__).resolve().parent / "Models"


def listar_modelos(pasta=DIRETORIO_MODELOS):
    """Retorna somente os modelos GGUF, em uma ordem estável."""
    return sorted(Path(pasta).glob("*.gguf"))


def Mostrar_Modelos(modelos, saida=print):
    """Mostra a mesma lista que será usada para resolver a escolha do usuário."""
    saida("Modelos disponíveis:")
    for numero, arquivo in enumerate(modelos, start=1):
        saida(f"[{numero}] - {arquivo.name}")


def carregar_modelo(entrada=input, saida=print, pasta=DIRETORIO_MODELOS):
    """Pede um número de modelo válido e devolve seu caminho.

    A listagem e a seleção usam a mesma coleção de arquivos .gguf. Assim, um
    arquivo auxiliar dentro de Models/ nunca desloca a numeração exibida.
    """
    modelos = listar_modelos(pasta)
    if not modelos:
        saida("Nenhum modelo .gguf foi encontrado na pasta Models.")
        return None

    Mostrar_Modelos(modelos, saida)

    while True:
        numero_digitado = entrada("Digite o número do modelo que deseja carregar: ").strip()
        try:
            indice = int(numero_digitado) - 1
        except ValueError:
            saida("Digite apenas o número de um modelo listado.")
            continue

        if 0 <= indice < len(modelos):
            return modelos[indice]

        saida(f"Escolha um número entre 1 e {len(modelos)}.")


def checar_tamanho(path):
    return CHK.checar_tamanho(path)


def exibir_abertura():
    init()

    logo = [
        (Fore.LIGHTCYAN_EX, "   ______________________      /\\"),
        (Fore.CYAN, "            ________          \\/"),
        (Fore.LIGHTBLUE_EX, "            ______            /\\"),
        (Fore.BLUE, "   _____________________)"),
    ]

    for cor, linha in logo:
        print(cor + linha)

    print(Style.RESET_ALL)
    print("=" * 30)
    print("Dragonic 4456 Console V0.3")
    print("\nOlá! Bem-vindo ao Dragonic 4456!")
    print("Por favor, aguarde\n")

    for i in range(21):
        barra = "#" * i + " " * (20 - i)
        porcentagem = i * 5
        sys.stdout.write(f"\r[{barra}] {porcentagem}%")
        sys.stdout.flush()
        time.sleep(0.15)

    print("\nSistema pronto!")


def main():
    exibir_abertura()
    enter = input("Pressione ENTER para começar ou qualquer coisa para sair: ")

    if enter != "":
        return

    path = carregar_modelo()
    if path is None:
        return

    if checar_tamanho(path):
        modelo = CM.carregar_modelo(path)
        CH.chat(modelo)
    else:
        print("Saindo...")


if __name__ == "__main__":
    main()
