from llama_cpp import Llama 
import contextlib
import os

# Função que carrega o modelo
def carregar_modelo(caminho):
    
    with open(os.devnull, "w") as fnull, contextlib.redirect_stderr(fnull):
        llm = Llama(
            
            model_path=str(caminho),
                
            # contexto de 600 tokens
            n_ctx=2048,  
                
            # desativa mensagens de log detalhadas   
            verbose=False 
        )
    return llm