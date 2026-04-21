def chat(modelo):
    while True:
        # solicita ao usuário que digite uma pergunta
        pergunta = input("Você: ") 
        if pergunta.lower() in  ["sair", "exit", "quit"]:
            print("Encerrando o chat. Até mais!")
            break

        # gera uma resposta usando o modelo carregado
        resposta = modelo(
            prompt = f"""System: Você é uma assistente útil, educada e inteligente.
            esponda em português de forma natural.
            Não repita frases desnecessariamente.
            Não gere símbolos aleatórios.
            Seja clara e amigável.

            Usuário: {pergunta}
            Assistente:""",
            max_tokens=80,
            temperature=0.2,
            stop=["Usuário:", "\n\n"],
            echo=False
        ) 
        # exibe a resposta gerada pelo modelo
        print("Model:", resposta["choices"][0]["text"].strip()) 