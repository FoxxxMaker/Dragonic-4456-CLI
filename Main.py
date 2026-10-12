import sys
import time
from pathlib import Path

from colorama import Fore, Style, init

import Carregar_Modelo as CM
import Chat as CH
import Checar_Tamanho as CHK
import Interface_CLI as INTERFACE


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
    """Pede um número de modelo válido e devolve seu caminho."""
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
    INTERFACE.limpar_tela()
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
    print("Dragonic 4456 Console V0.3 // BIOS MODE")
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
    input("Pressione ENTER para acessar o console: ")

    while True:
        escolha = INTERFACE.mostrar_menu_principal()
        if escolha == "1":
            path = carregar_modelo()
            if path is None:
                input("Pressione ENTER para voltar ao console: ")
                continue

            if checar_tamanho(path):
                modelo = CM.carregar_modelo(path)
                CH.chat(modelo)
            else:
                INTERFACE.mostrar_mensagem("Modelo acima do tamanho permitido.")
                input("Pressione ENTER para voltar ao console: ")
        elif escolha == "2":
            INTERFACE.mostrar_configuracao(CH.config)
            input("Pressione ENTER para voltar ao console: ")
        elif escolha == "3":
            INTERFACE.mostrar_mensagem("Dragonic desligado. Até a próxima!")
            return
        else:
            INTERFACE.mostrar_mensagem("Opção inválida. Escolha 1, 2 ou 3.")
            input("Pressione ENTER para tentar novamente: ")


if __name__ == "__main__":
    main()
