"""Backup local e legível das conversas do Dragonic."""

import json
from datetime import datetime
from pathlib import Path


RAIZ_PROJETO = Path(__file__).resolve().parent


def resolver_diretorio_backup(diretorio):
    """Resolve um diretório relativo a partir da pasta do projeto."""
    caminho = Path(diretorio)
    if not caminho.is_absolute():
        caminho = RAIZ_PROJETO / caminho
    return caminho


def salvar_backup(historico, system_prompt, diretorio="backups_chats", momento=None):
    """Salva uma sessão completa em JSON e retorna o caminho criado."""
    if not historico:
        return None

    momento = momento or datetime.now()
    pasta_backup = resolver_diretorio_backup(diretorio)
    pasta_backup.mkdir(parents=True, exist_ok=True)

    nome_arquivo = f"chat_{momento.strftime('%Y-%m-%d_%H-%M-%S_%f')}.json"
    caminho_backup = pasta_backup / nome_arquivo
    caminho_temporario = caminho_backup.with_suffix(".tmp")
    conteudo = {
        "formato": "dragonic-chat-backup-v1",
        "criado_em": momento.isoformat(timespec="seconds"),
        "system_prompt": system_prompt,
        "mensagens": historico,
    }

    with caminho_temporario.open("w", encoding="utf-8") as arquivo:
        json.dump(conteudo, arquivo, ensure_ascii=False, indent=2)
        arquivo.write("\n")

    caminho_temporario.replace(caminho_backup)
    return caminho_backup


def listar_backups(diretorio="backups_chats"):
    """Lista os backups mais recentes primeiro."""
    pasta_backup = resolver_diretorio_backup(diretorio)
    if not pasta_backup.exists():
        return []
    return sorted(pasta_backup.glob("chat_*.json"), reverse=True)


def carregar_backup(caminho):
    """Lê e valida o formato de um backup salvo pelo Dragonic."""
    with Path(caminho).open("r", encoding="utf-8") as arquivo:
        backup = json.load(arquivo)
    if backup.get("formato") != "dragonic-chat-backup-v1" or not isinstance(backup.get("mensagens"), list):
        raise ValueError("O arquivo não é um backup válido do Dragonic.")
    return backup
