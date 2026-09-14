"""Funções para manter o contexto da conversa durante a sessão atual.

Este módulo não salva nada em disco e não depende de banco de dados. Quando a
persistência existir, as funções de leitura e gravação podem ficar na camada
que chama estas funções.
"""


def criar_historico():
    """Cria uma lista vazia de mensagens para um novo chat."""
    return []


def adicionar_mensagem(historico, papel, conteudo, limite_mensagens):
    """Adiciona uma mensagem e mantém apenas o número de mensagens definido."""
    historico.append({"papel": papel, "conteudo": conteudo})

    if limite_mensagens is not None and limite_mensagens > 0:
        del historico[:-limite_mensagens]


def montar_prompt(system_prompt, historico, pergunta_atual):
    """Monta o prompt com o contexto anterior e a nova pergunta do usuário."""
    papeis = {
        "usuario": "Usuário",
        "assistente": "Assistente",
    }

    linhas = [system_prompt]
    for mensagem in historico:
        papel = papeis[mensagem["papel"]]
        linhas.append(f"{papel}: {mensagem['conteudo']}")

    linhas.append(f"Usuário: {pergunta_atual}")
    linhas.append("Assistente:")
    return "\n\n".join(linhas)
