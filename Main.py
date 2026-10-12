import sys
import time
from pathlib import Path

from colorama import Fore, Style, init

import Backup_Chat as BACKUP
import Benchmark
import Carregar_Modelo as CM
import Chat as CH
import Checar_Tamanho as CHK
import Interface_CLI as INTERFACE
import MCP_Integracoes as MCP_INTEGRACOES


DIRETORIO_MODELOS = Path(__file__).resolve().parent / "Models"


def listar_modelos(pasta=DIRETORIO_MODELOS):
    return sorted(Path(pasta).glob("*.gguf"))


def Mostrar_Modelos(modelos, saida=print):
    saida("Modelos disponíveis:")
    for numero, arquivo in enumerate(modelos, start=1):
        saida(f"[{numero}] - {arquivo.name}")


def carregar_modelo(entrada=input, saida=print, pasta=DIRETORIO_MODELOS):
    modelos = listar_modelos(pasta)
    if not modelos:
        saida("Nenhum modelo .gguf foi encontrado na pasta Models.")
        return None
    Mostrar_Modelos(modelos, saida)
    while True:
        try:
            indice = int(entrada("Digite o número do modelo que deseja carregar: ").strip()) - 1
        except ValueError:
            saida("Digite apenas o número de um modelo listado.")
            continue
        if 0 <= indice < len(modelos):
            return modelos[indice]
        saida(f"Escolha um número entre 1 e {len(modelos)}.")


def obter_modelo():
    path = carregar_modelo()
    if path is None or not CHK.checar_tamanho(path):
        return None
    return CM.carregar_modelo(path, CH.config.get("n_ctx", 2048)), path.name


def _salvar_alteracao(chave, valor):
    CH.config[chave] = valor
    CH.salvar_configuracao()


def _editar_numero(chave, tipo, minimo, rotulo):
    try:
        valor = tipo(input(f"Novo valor para {rotulo}: ").strip())
        if valor < minimo:
            raise ValueError
    except ValueError:
        INTERFACE.mostrar_mensagem(f"Use um número maior ou igual a {minimo}.")
        input("Pressione ENTER para continuar: ")
        return
    _salvar_alteracao(chave, valor)


def configurar_sistema():
    while True:
        INTERFACE.limpar_tela()
        INTERFACE.mostrar_configuracao(CH.config)
        escolha = input("Selecione o campo para alterar: ").strip().lower()
        if escolha == "0":
            return
        if escolha == "1":
            valor = input("Novo system prompt: ").strip()
            if valor:
                _salvar_alteracao("system_prompt", valor)
        elif escolha == "2":
            _editar_numero("temperature", float, 0.0, "temperatura")
        elif escolha == "3":
            _editar_numero("max_tokens", int, 1, "máximo de tokens")
        elif escolha == "4":
            _editar_numero("n_ctx", int, 128, "contexto do modelo")
        elif escolha == "5":
            _editar_numero("historico_max_mensagens", int, 0, "histórico no prompt")
        elif escolha == "6":
            valor = input("Stops separados por | (vazio remove todos): ")
            _salvar_alteracao("stop", [item.strip() for item in valor.split("|") if item.strip()])
        elif escolha == "7":
            _salvar_alteracao("echo", not CH.config["echo"])
        elif escolha == "8":
            _salvar_alteracao("backup_chats_habilitado", not CH.config.get("backup_chats_habilitado", True))
        elif escolha == "9":
            valor = input("Pasta de backup: ").strip()
            if valor:
                _salvar_alteracao("diretorio_backup_chats", valor)
        elif escolha == "b":
            carregado = obter_modelo()
            if carregado is not None:
                modelo, _ = carregado
                resultado = Benchmark.executar(modelo, CH.config)
                INTERFACE.mostrar_mensagem(
                    f"{resultado['tokens']} tokens em {resultado['duracao_segundos']:.2f}s "
                    f"({resultado['tokens_por_segundo']:.2f} tokens/s)."
                )
                input("Pressione ENTER para voltar às configurações: ")
        else:
            INTERFACE.mostrar_mensagem("Opção inválida.")
            input("Pressione ENTER para continuar: ")


def gerenciar_chats():
    backups = BACKUP.listar_backups(CH.config.get("diretorio_backup_chats", "backups_chats"))
    resumos = [f"[{indice}] {arquivo.name}" for indice, arquivo in enumerate(backups, start=1)]
    INTERFACE.limpar_tela()
    INTERFACE.mostrar_backups(resumos)
    if not backups:
        input("Pressione ENTER para voltar: ")
        return
    try:
        indice = int(input("Escolha um chat (0 para voltar): ")) - 1
    except ValueError:
        return
    if indice < 0 or indice >= len(backups):
        return
    try:
        backup = BACKUP.carregar_backup(backups[indice])
    except (OSError, ValueError):
        INTERFACE.mostrar_mensagem("Não foi possível abrir esse backup.")
        input("Pressione ENTER para voltar: ")
        return
    INTERFACE.limpar_tela()
    INTERFACE.mostrar_conversa(backup["mensagens"])
    if input("[1] Continuar este chat  [0] Voltar: ").strip() == "1":
        carregado = obter_modelo()
        if carregado is not None:
            modelo, nome_modelo = carregado
            CH.chat(
                modelo,
                historico_inicial=backup["mensagens"],
                system_prompt=backup.get("system_prompt"),
                nome_modelo=nome_modelo,
            )


def gerenciar_mcp():
    while True:
        servidores = MCP_INTEGRACOES.listar_servidores()
        INTERFACE.limpar_tela()
        INTERFACE.mostrar_mcp(
            CH.config.get("mcp_local_habilitado", True),
            servidores,
            MCP_INTEGRACOES.DIRETORIO_SERVIDORES,
        )
        escolha = input("Selecione uma opção MCP: ").strip()
        if escolha == "0":
            return
        if escolha == "1":
            _salvar_alteracao("mcp_local_habilitado", not CH.config.get("mcp_local_habilitado", True))
        elif escolha == "2":
            input("Pressione ENTER para voltar: ")
        elif escolha == "3":
            nome = input("Nome da integração: ")
            comando = input("Comando (ex.: npx): ")
            argumentos = [item.strip() for item in input("Argumentos separados por |: ").split("|") if item.strip()]
            try:
                MCP_INTEGRACOES.adicionar_servidor(nome, comando, argumentos)
            except ValueError as erro:
                INTERFACE.mostrar_mensagem(str(erro))
                input("Pressione ENTER para continuar: ")
        elif escolha == "4":
            try:
                MCP_INTEGRACOES.remover_servidor(input("Nome da integração para remover: "))
            except ValueError as erro:
                INTERFACE.mostrar_mensagem(str(erro))
                input("Pressione ENTER para continuar: ")
        elif escolha == "5":
            INTERFACE.mostrar_mensagem(f"Pasta MCP: {MCP_INTEGRACOES.DIRETORIO_SERVIDORES}")
            input("Pressione ENTER para voltar: ")
        else:
            INTERFACE.mostrar_mensagem("Opção MCP inválida.")
            input("Pressione ENTER para continuar: ")


def exibir_abertura():
    init()
    INTERFACE.limpar_tela()
    for cor, linha in [
        (Fore.LIGHTCYAN_EX, "   ______________________      /\\"),
        (Fore.CYAN, "            ________          \\/"),
        (Fore.LIGHTBLUE_EX, "            ______            /\\"),
        (Fore.BLUE, "   _____________________)"),
    ]:
        print(cor + linha)
    print(Style.RESET_ALL + "=" * 30)
    print("Dragonic 4456 Console V0.3 // BIOS MODE")
    for i in range(21):
        sys.stdout.write(f"\r[{'#' * i}{' ' * (20 - i)}] {i * 5}%")
        sys.stdout.flush()
        time.sleep(0.15)
    print("\nSistema pronto!")


def main():
    exibir_abertura()
    input("Pressione ENTER para acessar o console: ")
    while True:
        escolha = INTERFACE.mostrar_menu_principal()
        if escolha == "1":
            carregado = obter_modelo()
            if carregado is not None:
                modelo, nome_modelo = carregado
                CH.chat(modelo, nome_modelo=nome_modelo)
        elif escolha == "2":
            configurar_sistema()
        elif escolha == "3":
            gerenciar_chats()
        elif escolha == "4":
            gerenciar_mcp()
        elif escolha == "5":
            INTERFACE.mostrar_mensagem("Dragonic desligado. Até a próxima!")
            return
        else:
            INTERFACE.mostrar_mensagem("Opção inválida. Escolha 1, 2, 3, 4 ou 5.")
            input("Pressione ENTER para tentar novamente: ")


if __name__ == "__main__":
    main()
