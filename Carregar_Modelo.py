import contextlib
import os


def gpu_disponivel():
    """Informa se o wheel atual do llama.cpp foi compilado com offload de GPU."""
    try:
        from llama_cpp import llama_supports_gpu_offload
    except ImportError:
        return False
    return bool(llama_supports_gpu_offload())


def carregar_modelo(caminho, n_ctx=2048, n_gpu_layers=0):
    # Importa a dependência nativa apenas quando um modelo for realmente usado.
    # Assim, funções de seleção e testes não precisam inicializar llama.cpp.
    from llama_cpp import Llama

    if n_gpu_layers and not gpu_disponivel():
        raise RuntimeError(
            "A aceleração Vulkan foi selecionada, mas o llama-cpp-python atual é CPU. "
            "Execute install_windows.ps1 -Backend Vulkan para instalar o wheel Vulkan."
        )

    with open(os.devnull, "w") as fnull, contextlib.redirect_stderr(fnull):
        llm = Llama(
            model_path=str(caminho),
            n_ctx=n_ctx,
            n_gpu_layers=n_gpu_layers,
            verbose=False,
        )
    return llm
