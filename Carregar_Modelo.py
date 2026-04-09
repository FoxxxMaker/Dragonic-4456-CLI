from llama_cpp import Llama # Chama é uma biblioteca de código aberto para trabalhar com modelos de linguagem, como o LLaMA da Meta. A classe Llama é usada para carregar e interagir com esses modelos.

# Função que carrega o modelo
def carregar_modelo(caminho):
    llm = Llama(
        model_path=caminho,
        n_ctx=600, # contexto de 600 tokens 
        verbose=False # desativa mensagens de log detalhadas
    )
    return llm