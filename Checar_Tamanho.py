import os
import time

def checar_tamanho(caminho):
    tamanho = os.stat(caminho).st_size

    for i in range(20):
        os.system("cls" if os.name == "nt" else "clear")
        print("carregando modelo" + "." * (i + 1))
        time.sleep(0.5)

    if tamanho <= 900000000:
        return True
    else:
        return False