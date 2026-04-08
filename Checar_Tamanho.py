import os
import Main as M
import time


caminho = M.Path  # ainda não foi adicionado no arquivo Main uma forma de carregar.

tamanho = os.stat(caminho).st_size

for i in range(20):
    os.system("cls" if os.name == "nt" else "clear")
    print("carregando modelo" + "." * (i + 1))
    time.sleep(0.5)

if tamanho <= 900000000:
    pass
else:
    print("Erro, o arquivo é muito grande e não será usado.")
    exit()

