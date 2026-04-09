def chat(modelo):
    while True:
        # solicita ao usuário que digite uma pergunta
        pergunta = input("Você: ") 
        # gera uma resposta usando o modelo carregado
        resposta = modelo(pergunta) 
        # exibe a resposta gerada pelo modelo
        print("Model:", resposta["choices"][0]["text"].strip()) 