import Carregar_Modelo as CM

def chat(modelo):
    while True:
        pergunta = input("Você: ") # solicita ao usuário que digite uma pergunta
        resposta = modelo(pergunta) # gera uma resposta usando o modelo carregado
        print("Model:", resposta["choices"][0]["text"].strip()) # exibe a resposta gerada pelo modelo