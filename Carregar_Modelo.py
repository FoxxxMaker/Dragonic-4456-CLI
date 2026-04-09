"""

import torch
import Checar_Tamanho as CHK

# Carrega o modelo

local = CHK.caminho

#Usa o modelo torchscript para carregar
modelo = torch.load(local, map_location="cpu")

"""