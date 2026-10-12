import contextlib
import os


def carregar_modelo(caminho):
    # Importa a dependência nativa apenas quando um modelo for realmente usado.
    # Assim, funções de seleção e testes não precisam inicializar llama.cpp.
    from llama_cpp import Llama

    with open(os.devnull, "w") as fnull, contextlib.redirect_stderr(fnull):
        llm = Llama(
            model_path=str(caminho),
            n_ctx=2048,
            verbose=False,
        )
    return llm
