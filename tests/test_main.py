import importlib
import os
import tempfile
import unittest
from pathlib import Path

import Chat
import Main


class SelecaoDeModeloTests(unittest.TestCase):
    def test_listar_modelos_ignora_arquivos_auxiliares_e_ordena(self):
        with tempfile.TemporaryDirectory() as diretorio_temporario:
            pasta = Path(diretorio_temporario)
            (pasta / "zeta.gguf").touch()
            (pasta / "Model.txt").touch()
            (pasta / "alpha.gguf").touch()

            modelos = Main.listar_modelos(pasta)

        self.assertEqual([modelo.name for modelo in modelos], ["alpha.gguf", "zeta.gguf"])

    def test_carregar_modelo_rejeita_entrada_invalida_ate_receber_numero_valido(self):
        with tempfile.TemporaryDirectory() as diretorio_temporario:
            pasta = Path(diretorio_temporario)
            (pasta / "primeiro.gguf").touch()
            (pasta / "segundo.gguf").touch()
            entradas = iter(["texto", "3", "2"])
            mensagens = []

            modelo = Main.carregar_modelo(
                entrada=lambda _: next(entradas),
                saida=mensagens.append,
                pasta=pasta,
            )

        self.assertEqual(modelo.name, "segundo.gguf")
        self.assertIn("[1] - primeiro.gguf", mensagens)
        self.assertIn("[2] - segundo.gguf", mensagens)
        self.assertIn("Digite apenas o número de um modelo listado.", mensagens)
        self.assertIn("Escolha um número entre 1 e 2.", mensagens)

    def test_carregar_modelo_sem_arquivos_retorna_none(self):
        with tempfile.TemporaryDirectory() as diretorio_temporario:
            mensagens = []

            modelo = Main.carregar_modelo(
                entrada=lambda _: self.fail("Não deveria solicitar uma escolha sem modelos."),
                saida=mensagens.append,
                pasta=diretorio_temporario,
            )

        self.assertIsNone(modelo)
        self.assertEqual(mensagens, ["Nenhum modelo .gguf foi encontrado na pasta Models."])

    def test_chat_carrega_configuracao_mesmo_fora_da_pasta_do_projeto(self):
        diretorio_original = Path.cwd()
        with tempfile.TemporaryDirectory() as diretorio_temporario:
            try:
                os.chdir(diretorio_temporario)
                chat_recarregado = importlib.reload(Chat)
            finally:
                os.chdir(diretorio_original)

        self.assertIn("system_prompt", chat_recarregado.config)

    def test_obter_modelo_envia_configuracao_de_gpu_ao_carregador(self):
        configuracao_original = Chat.config
        carregar_original = Main.carregar_modelo
        checar_original = Main.CHK.checar_tamanho
        modelo_original = Main.CM.carregar_modelo
        caminho = Path("modelo.gguf")
        argumentos = []
        Chat.config = {**configuracao_original, "n_ctx": 4096, "n_gpu_layers": -1}
        Main.carregar_modelo = lambda: caminho
        Main.CHK.checar_tamanho = lambda _: True
        Main.CM.carregar_modelo = lambda *args: argumentos.append(args) or "modelo"
        try:
            resultado = Main.obter_modelo()
        finally:
            Chat.config = configuracao_original
            Main.carregar_modelo = carregar_original
            Main.CHK.checar_tamanho = checar_original
            Main.CM.carregar_modelo = modelo_original

        self.assertEqual(resultado, ("modelo", "modelo.gguf"))
        self.assertEqual(argumentos, [(caminho, 4096, -1)])


if __name__ == "__main__":
    unittest.main()
