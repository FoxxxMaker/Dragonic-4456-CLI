import json
from pathlib import Path

import Backup_Chat as BACKUP
import Chat_Historico as HISTORICO


CAMINHO_CONFIGURACAO = Path(__file__).resolve().parent / "Config.json"

with CAMINHO_CONFIGURACAO.open("r", encoding="utf-8") as arquivo:
    config = json.load(arquivo)


def salvar_configuracao():
    """Persiste as configurações atuais sem depender da pasta do terminal."""
    caminho_temporario = CAMINHO_CONFIGURACAO.with_suffix(".tmp")
    with caminho_temporario.open("w", encoding="utf-8") as arquivo:
        json.dump(config, arquivo, ensure_ascii=False, indent=2)
        arquivo.write("\n")
    caminho_temporario.replace(CAMINHO_CONFIGURACAO)


def chat(modelo, entrada=input, saida=print, historico_inicial=None, system_prompt=None):
    """Executa um chat novo ou retomado e salva sua sessão ao encerrar."""
    historico_backup = list(historico_inicial or [])
    limite_mensagens = config.get("historico_max_mensagens", 10)
    historico_contexto = historico_backup[-limite_mensagens:] if limite_mensagens > 0 else []
    system_prompt = system_prompt or config["system_prompt"]

    try:
        while True:
            pergunta = entrada("Você: ")
            if pergunta.lower() in ["sair", "exit", "quit"]:
                saida("Encerrando o chat. Até mais!")
                break

            prompt = HISTORICO.montar_prompt(system_prompt, historico_contexto, pergunta)
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
                system_prompt,
                config.get("diretorio_backup_chats", "backups_chats"),
            )
            if caminho_backup is not None:
                saida(f"Backup salvo em: {caminho_backup}")
