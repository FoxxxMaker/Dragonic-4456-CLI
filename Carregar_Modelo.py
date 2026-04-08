import torch
import Main as M

# Carrega o modelo

caminho = M.Path # ainda não foi adicionado no arquivo Main uma forma de carregar.

#Usa o modelo torchscript para carregar
modelo = torch.load(caminho, map_location="cpu")