"""Benchmark curto para verificar a geração do modelo carregado."""

from time import perf_counter


PROMPT_BENCHMARK = "Responda somente: benchmark concluído."


def executar(modelo, configuracao):
    inicio = perf_counter()
    resposta = modelo(
        prompt=PROMPT_BENCHMARK,
        max_tokens=min(configuracao["max_tokens"], 32),
        temperature=0.0,
        stop=configuracao["stop"],
        echo=False,
    )
    duracao = perf_counter() - inicio
    texto = resposta["choices"][0]["text"].strip()
    tokens = resposta.get("usage", {}).get("completion_tokens", len(texto.split()))
    return {
        "duracao_segundos": duracao,
        "tokens": tokens,
        "tokens_por_segundo": tokens / duracao if duracao else 0.0,
        "texto": texto,
    }
