"""Cadastro local de servidores MCP externos por stdio."""

import json
from pathlib import Path


DIRETORIO_SERVIDORES = Path(__file__).resolve().parent / "MCP_Servers"
ARQUIVO_CONFIGURACAO = DIRETORIO_SERVIDORES / "servidores.json"


def _garantir_pasta():
    DIRETORIO_SERVIDORES.mkdir(exist_ok=True)


def listar_servidores():
    _garantir_pasta()
    if not ARQUIVO_CONFIGURACAO.exists():
        return []
    with ARQUIVO_CONFIGURACAO.open("r", encoding="utf-8") as arquivo:
        return json.load(arquivo).get("servidores", [])


def salvar_servidores(servidores):
    _garantir_pasta()
    temporario = ARQUIVO_CONFIGURACAO.with_suffix(".tmp")
    with temporario.open("w", encoding="utf-8") as arquivo:
        json.dump({"servidores": servidores}, arquivo, ensure_ascii=False, indent=2)
        arquivo.write("\n")
    temporario.replace(ARQUIVO_CONFIGURACAO)


def adicionar_servidor(nome, comando, argumentos):
    nome, comando = nome.strip(), comando.strip()
    if not nome or not comando:
        raise ValueError("Nome e comando são obrigatórios.")
    servidores = listar_servidores()
    if any(servidor["nome"].lower() == nome.lower() for servidor in servidores):
        raise ValueError("Já existe uma integração com esse nome.")
    servidores.append({"nome": nome, "comando": comando, "argumentos": argumentos, "habilitado": True})
    salvar_servidores(servidores)


def remover_servidor(nome):
    servidores = listar_servidores()
    restantes = [servidor for servidor in servidores if servidor["nome"].lower() != nome.lower()]
    if len(restantes) == len(servidores):
        raise ValueError("Integração não encontrada.")
    salvar_servidores(restantes)
