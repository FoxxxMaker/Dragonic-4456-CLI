"""Painéis de terminal inspirados em interfaces BIOS."""

import os

from colorama import Fore, Style


LARGURA = 76


def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def _borda():
    return f"{Fore.LIGHTCYAN_EX}╠{'═' * (LARGURA - 2)}╣{Style.RESET_ALL}"


def _linha(texto=""):
    texto = str(texto)[: LARGURA - 4]
    return f"{Fore.LIGHTCYAN_EX}║{Style.RESET_ALL} {texto:<{LARGURA - 4}} {Fore.LIGHTCYAN_EX}║{Style.RESET_ALL}"


def painel(titulo, linhas, saida=print):
    saida(f"{Fore.LIGHTCYAN_EX}╔{'═' * (LARGURA - 2)}╗{Style.RESET_ALL}")
    saida(_linha(f"DRAGONIC 4456 // {titulo.upper()}"))
    saida(_borda())
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
            "[2] Configurações do sistema",
            "[3] Visualizar ou continuar chats salvos",
            "[4] Desligar Dragonic",
        ],
        saida,
    )
    return entrada("Selecione uma opção: ").strip()


def mostrar_configuracao(configuracao, saida=print):
    painel(
        "configurações editáveis",
        [
            f"System prompt: {configuracao['system_prompt']}",
            f"[1] Temperatura: {configuracao['temperature']}",
            f"[2] Máximo de tokens: {configuracao['max_tokens']}",
            f"[3] Contexto do modelo (n_ctx): {configuracao.get('n_ctx', 2048)}",
            f"[4] Histórico no prompt: {configuracao.get('historico_max_mensagens', 10)} mensagens",
            f"[5] Stop: {' | '.join(configuracao['stop']) or '(nenhum)'}",
            f"[6] Echo: {'ATIVADO' if configuracao['echo'] else 'DESATIVADO'}",
            f"[7] Backup: {'ATIVADO' if configuracao.get('backup_chats_habilitado', True) else 'DESATIVADO'}",
            f"[8] Pasta de backup: {configuracao.get('diretorio_backup_chats', 'backups_chats')}",
            "[9] Editar system prompt",
            "[B] Rodar benchmark de modelo     [0] Voltar",
        ],
        saida,
    )


def mostrar_backups(resumos, saida=print):
    painel("chats salvos", resumos or ["Nenhum backup de chat encontrado."], saida)


def mostrar_conversa(mensagens, saida=print):
    linhas = []
    for mensagem in mensagens[-12:]:
        papel = "Você" if mensagem.get("papel") == "usuario" else "Model"
        texto = mensagem.get("conteudo", "").replace("\n", " ")
        linhas.append(f"{papel}: {texto}")
    painel("visualização de chat (últimas 12 mensagens)", linhas or ["Conversa vazia."], saida)


def mostrar_mensagem(mensagem, saida=print):
    painel("mensagem do sistema", [mensagem], saida)
