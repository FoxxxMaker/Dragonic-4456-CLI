"""Painéis de terminal inspirados em interfaces BIOS."""

import os

from colorama import Fore, Style


LARGURA = 68


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def _borda():
    return f"{Fore.LIGHTCYAN_EX}╠{'═' * (LARGURA - 2)}╣{Style.RESET_ALL}"


def _linha(texto=""):
    texto = str(texto)[: LARGURA - 4]
    return f"{Fore.LIGHTCYAN_EX}║{Style.RESET_ALL} {texto:<{LARGURA - 4}} {Fore.LIGHTCYAN_EX}║{Style.RESET_ALL}"


def cabecalho(titulo, saida=print):
    saida(f"{Fore.LIGHTCYAN_EX}╔{'═' * (LARGURA - 2)}╗{Style.RESET_ALL}")
    saida(_linha(f"DRAGONIC 4456 // {titulo.upper()}"))
    saida(_borda())


def painel(titulo, linhas, saida=print):
    cabecalho(titulo, saida)
    for linha in linhas:
        saida(_linha(linha))
    saida(f"{Fore.LIGHTCYAN_EX}╚{'═' * (LARGURA - 2)}╝{Style.RESET_ALL}")


def mostrar_menu_principal(entrada=input, saida=print, limpar=limpar_tela):
    limpar()
    painel(
        "console de controle",
        [
            "STATUS: SISTEMA PRONTO",
            "",
            "[1] Inicializar chat local",
            "[2] Ver configuração do sistema",
            "[3] Desligar Dragonic",
        ],
        saida,
    )
    return entrada("Selecione uma opção: ").strip()


def mostrar_configuracao(configuracao, saida=print):
    painel(
        "configuração do sistema",
        [
            f"Tokens máximos: {configuracao['max_tokens']}",
            f"Temperatura: {configuracao['temperature']}",
            f"Histórico no contexto: {configuracao.get('historico_max_mensagens', 10)} mensagens",
            f"Backup de chats: {'ATIVADO' if configuracao.get('backup_chats_habilitado', True) else 'DESATIVADO'}",
            f"Pasta de backup: {configuracao.get('diretorio_backup_chats', 'backups_chats')}",
        ],
        saida,
    )


def mostrar_mensagem(mensagem, saida=print):
    painel("mensagem do sistema", [mensagem], saida)
