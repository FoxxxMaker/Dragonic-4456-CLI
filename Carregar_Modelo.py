from llama_cpp import Llama 
import contextlib
import os

# Função que carrega o modelo
def carregar_modelo(caminho):
    
    with open(os.devnull, "w") as fnull, contextlib.redirect_stderr(fnull):
        llm = Llama(
            
            model_path=caminho,
                
            # contexto de 600 tokens
            n_ctx=600,  
                
            # desativa mensagens de log detalhadas   
            verbose=False 
        )
    return llm