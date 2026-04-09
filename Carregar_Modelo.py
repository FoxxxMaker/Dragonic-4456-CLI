from llama_cpp import Llama 

# Função que carrega o modelo
def carregar_modelo(caminho):
    llm = Llama(
        model_path=caminho,
        
        # contexto de 600 tokens
        n_ctx=600,  
        
        # desativa mensagens de log detalhadas   
        verbose=False 
    )
    return llm