import os
import time

def checar_tamanho(caminho):
    tamanho = os.stat(caminho).st_size

    if tamanho <= 900 * 1024 * 1024:
        for i in range(20):
            os.system("cls" if os.name == "nt" else "clear")
            print("carregando modelo" + "." * (i + 1))
            time.sleep(0.5)
        return True
    else:
        return False

    

    