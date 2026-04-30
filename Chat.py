import json
    
with open("Config.json", "r") as f:
    config = json.load(f)

def chat(modelo):
    while True:
        # solicita ao usuário que digite uma pergunta
        pergunta = input("Você: ") 
        if pergunta.lower() in  ["sair", "exit", "quit"]:
            print("Encerrando o chat. Até mais!")
            break

        # gera uma resposta usando o modelo carregado e as configurações do arquivo JSON
        resposta = modelo(
            prompt=config["system_prompt"] + "\n\n" + "Usuário: " + pergunta + "\n\n",
            max_tokens=config["max_tokens"],
            temperature=config["temperature"],
            stop=config["stop"],
            echo=config["echo"]
        ) 
        # exibe a resposta gerada pelo modelo
        print("Model:", resposta["choices"][0]["text"].strip()) 