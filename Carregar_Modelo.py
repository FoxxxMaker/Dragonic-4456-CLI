from llama_cpp import Llama 

# Função que carrega o modelo
def carregar_modelo(caminho):
    llm = Llama(
        model_path=caminho,
        n_ctx=600, # contexto de 600 tokens 
        verbose=False # desativa mensagens de log detalhadas
    )
    return llm