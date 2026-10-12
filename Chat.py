import json
from pathlib import Path

import Backup_Chat as BACKUP
import Chat_Historico as HISTORICO


CAMINHO_CONFIGURACAO = Path(__file__).resolve().parent / "Config.json"

with CAMINHO_CONFIGURACAO.open("r", encoding="utf-8") as arquivo:
    config = json.load(arquivo)


def chat(modelo, entrada=input, saida=print):
    """Executa o chat e cria um backup ao encerrar uma sessão com mensagens."""
    historico_contexto = HISTORICO.criar_historico()
    historico_backup = HISTORICO.criar_historico()
    limite_mensagens = config.get("historico_max_mensagens", 10)

    try:
        while True:
            pergunta = entrada("Você: ")
            if pergunta.lower() in ["sair", "exit", "quit"]:
                saida("Encerrando o chat. Até mais!")
                break

            prompt = HISTORICO.montar_prompt(
                config["system_prompt"],
                historico_contexto,
                pergunta,
            )
            resposta = modelo(
                prompt=prompt,
                max_tokens=config["max_tokens"],
                temperature=config["temperature"],
                stop=config["stop"],
                echo=config["echo"],
            )
            texto_resposta = resposta["choices"][0]["text"].strip()

            for historico, limite in (
                (historico_contexto, limite_mensagens),
                (historico_backup, None),
            ):
                HISTORICO.adicionar_mensagem(historico, "usuario", pergunta, limite)
                HISTORICO.adicionar_mensagem(historico, "assistente", texto_resposta, limite)

            saida(f"Model: {texto_resposta}")
    except (EOFError, KeyboardInterrupt):
        saida("Chat interrompido. Salvando a conversa atual...")
    finally:
        if config.get("backup_chats_habilitado", True):
            caminho_backup = BACKUP.salvar_backup(
                historico_backup,
                config["system_prompt"],
                config.get("diretorio_backup_chats", "backups_chats"),
            )
            if caminho_backup is not None:
                saida(f"Backup salvo em: {caminho_backup}")
