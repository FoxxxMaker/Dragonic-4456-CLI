import json
from pathlib import Path

import Backup_Chat as BACKUP
import Chat_Historico as HISTORICO
import MCP_Local as MCP


CAMINHO_CONFIGURACAO = Path(__file__).resolve().parent / "Config.json"

with CAMINHO_CONFIGURACAO.open("r", encoding="utf-8") as arquivo:
    config = json.load(arquivo)


def salvar_configuracao():
    caminho_temporario = CAMINHO_CONFIGURACAO.with_suffix(".tmp")
    with caminho_temporario.open("w", encoding="utf-8") as arquivo:
        json.dump(config, arquivo, ensure_ascii=False, indent=2)
        arquivo.write("\n")
    caminho_temporario.replace(CAMINHO_CONFIGURACAO)


def exibir_historico(historico, saida=print):
    if not historico:
        return
    saida("\n=== CHAT RETOMADO: MENSAGENS ANTERIORES ===")
    for mensagem in historico:
        papel = "Você" if mensagem.get("papel") == "usuario" else "Model"
        saida(f"{papel}: {mensagem.get('conteudo', '')}")
    saida("=== FIM DO HISTÓRICO ===\n")


def _gerar(modelo, prompt):
    resposta = modelo(
        prompt=prompt,
        max_tokens=config["max_tokens"],
        temperature=config["temperature"],
        stop=config["stop"],
        echo=config["echo"],
    )
    return resposta["choices"][0]["text"].strip()


def gerar_resposta(modelo, prompt):
    """Gera a resposta e executa no máximo uma ferramenta MCP por turno."""
    texto = _gerar(modelo, prompt)
    chamada = MCP.extrair_chamada(texto)
    if chamada is None:
        return texto

    nome, argumentos = chamada
    resultado = MCP.chamar_ferramenta(nome, argumentos)
    texto_resultado = resultado["content"][0]["text"]
    prompt_com_resultado = (
        f"{prompt}\n\nResultado da ferramenta MCP {nome}: {texto_resultado}"
        "\n\nAgora responda ao usuário usando esse resultado.\nAssistente:"
    )
    return _gerar(modelo, prompt_com_resultado)


def chat(modelo, entrada=input, saida=print, historico_inicial=None, system_prompt=None, nome_modelo=None):
    """Executa um chat novo ou retomado e salva sua sessão ao encerrar."""
    historico_backup = list(historico_inicial or [])
    limite_mensagens = config.get("historico_max_mensagens", 10)
    historico_contexto = historico_backup[-limite_mensagens:] if limite_mensagens > 0 else []
    system_prompt = system_prompt or config["system_prompt"]
    prompt_com_mcp = system_prompt
    if config.get("mcp_local_habilitado", True):
        prompt_com_mcp += MCP.instrucao_para_modelo()

    if nome_modelo:
        saida(nome_modelo)
    exibir_historico(historico_backup, saida)

    try:
        while True:
            pergunta = entrada("Você: ")
            if pergunta.lower() in ["sair", "exit", "quit"]:
                saida("Encerrando o chat. Até mais!")
                break
            if pergunta.strip() == "/mcp":
                if config.get("mcp_local_habilitado", True):
                    saida("Ferramentas MCP: " + ", ".join(item["name"] for item in MCP.listar_ferramentas()))
                else:
                    saida("O MCP local está desativado nas configurações.")
                continue

            prompt = HISTORICO.montar_prompt(prompt_com_mcp, historico_contexto, pergunta)
            texto_resposta = gerar_resposta(modelo, prompt)
            for historico, limite in ((historico_contexto, limite_mensagens), (historico_backup, None)):
                HISTORICO.adicionar_mensagem(historico, "usuario", pergunta, limite)
                HISTORICO.adicionar_mensagem(historico, "assistente", texto_resposta, limite)
            saida(f"Model: {texto_resposta}")
    except (EOFError, KeyboardInterrupt):
        saida("Chat interrompido. Salvando a conversa atual...")
    finally:
        if config.get("backup_chats_habilitado", True):
            caminho_backup = BACKUP.salvar_backup(
                historico_backup,
                system_prompt,
                config.get("diretorio_backup_chats", "backups_chats"),
            )
            if caminho_backup is not None:
                saida(f"Backup salvo em: {caminho_backup}")
