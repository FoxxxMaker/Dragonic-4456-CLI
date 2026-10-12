import json
from pathlib import Path

import Chat_Historico as HISTORICO


CAMINHO_CONFIGURACAO = Path(__file__).resolve().parent / "Config.json"


with CAMINHO_CONFIGURACAO.open("r", encoding="utf-8") as f:
    config = json.load(f)

def chat(modelo):
    historico = HISTORICO.criar_historico()
    limite_mensagens = config.get("historico_max_mensagens", 10)

    while True:
        # solicita ao usuário que digite uma pergunta
        pergunta = input("Você: ") 
        if pergunta.lower() in  ["sair", "exit", "quit"]:
            print("Encerrando o chat. Até mais!")
            break

        prompt = HISTORICO.montar_prompt(
            config["system_prompt"],
            historico,
            pergunta
        )

        # gera uma resposta usando o modelo carregado e as configurações do arquivo JSON
        resposta = modelo(
            prompt=prompt,
            max_tokens=config["max_tokens"],
            temperature=config["temperature"],
            stop=config["stop"],
            echo=config["echo"]
        ) 
        texto_resposta = resposta["choices"][0]["text"].strip()

        HISTORICO.adicionar_mensagem(
            historico,
            "usuario",
            pergunta,
            limite_mensagens
        )
        HISTORICO.adicionar_mensagem(
            historico,
            "assistente",
            texto_resposta,
            limite_mensagens
        )

        # exibe a resposta gerada pelo modelo
        print("Model:", texto_resposta)
