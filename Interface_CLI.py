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
            "[4] MCP local e integrações",
            "[5] Desligar Dragonic",
        ],
        saida,
    )
    return entrada("Selecione uma opção: ").strip()


def mostrar_configuracao(configuracao, saida=print):
    painel(
        "configurações editáveis",
        [
            f"[1] System prompt: {configuracao['system_prompt']}",
            f"[2] Temperatura: {configuracao['temperature']}",
            f"[3] Máximo de tokens: {configuracao['max_tokens']}",
            f"[4] Contexto do modelo (n_ctx): {configuracao.get('n_ctx', 2048)}",
            f"[5] Histórico no prompt: {configuracao.get('historico_max_mensagens', 10)} mensagens",
            f"[6] Stop: {' | '.join(configuracao['stop']) or '(nenhum)'}",
            f"[7] Echo: {'ATIVADO' if configuracao['echo'] else 'DESATIVADO'}",
            f"[8] Backup: {'ATIVADO' if configuracao.get('backup_chats_habilitado', True) else 'DESATIVADO'}",
            f"[9] Pasta de backup: {configuracao.get('diretorio_backup_chats', 'backups_chats')}",
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


def mostrar_mcp(local_habilitado, servidores, pasta, saida=print):
    linhas = [
        f"MCP local: {'ATIVADO' if local_habilitado else 'DESATIVADO'}",
        f"Pasta de integrações: {pasta}",
        "",
        "[1] Ativar/desativar MCP local",
        "[2] Listar integrações externas",
        "[3] Adicionar servidor MCP stdio",
        "[4] Remover integração",
        "[5] Mostrar caminho da pasta",
        "[0] Voltar",
    ]
    linhas.extend(
        f"- {servidor['nome']} ({'ativo' if servidor.get('habilitado', True) else 'inativo'})"
        for servidor in servidores
    )
    painel("mcp e integrações", linhas, saida)


def mostrar_mensagem(mensagem, saida=print):
    painel("mensagem do sistema", [mensagem], saida)
