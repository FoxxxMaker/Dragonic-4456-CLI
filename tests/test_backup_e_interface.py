import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

import Backup_Chat
import Chat
import Interface_CLI


class BackupChatTests(unittest.TestCase):
    def test_salvar_backup_preserva_todas_as_mensagens_em_json_utf8(self):
        mensagens = [
            {"papel": "usuario", "conteudo": "Olá"},
            {"papel": "assistente", "conteudo": "Oi, lobo!"},
        ]
        with tempfile.TemporaryDirectory() as diretorio_temporario:
            caminho = Backup_Chat.salvar_backup(
                mensagens,
                "Sistema de teste",
                diretorio_temporario,
                momento=datetime(2026, 10, 12, 14, 30, 0, 1),
            )
            conteudo = json.loads(caminho.read_text(encoding="utf-8"))

        self.assertEqual(conteudo["formato"], "dragonic-chat-backup-v1")
        self.assertEqual(conteudo["mensagens"], mensagens)
        self.assertEqual(caminho.name, "chat_2026-10-12_14-30-00_000001.json")

    def test_chat_cria_backup_completo_mesmo_quando_contexto_e_limitado(self):
        configuracao_original = Chat.config
        with tempfile.TemporaryDirectory() as diretorio_temporario:
            Chat.config = {
                **configuracao_original,
                "historico_max_mensagens": 1,
                "backup_chats_habilitado": True,
                "diretorio_backup_chats": diretorio_temporario,
            }
            entradas = iter(["primeira", "segunda", "sair"])
            saidas = []

            def modelo(**_):
                return {"choices": [{"text": "resposta"}]}

            try:
                Chat.chat(modelo, entrada=lambda _: next(entradas), saida=saidas.append)
            finally:
                Chat.config = configuracao_original

            arquivos = list(Path(diretorio_temporario).glob("*.json"))
            conteudo = json.loads(arquivos[0].read_text(encoding="utf-8"))

        self.assertEqual(len(arquivos), 1)
        self.assertEqual(len(conteudo["mensagens"]), 4)
        self.assertIn("Backup salvo em:", "\n".join(saidas))


class InterfaceCliTests(unittest.TestCase):
    def test_menu_exibe_opcoes_e_retorna_escolha(self):
        saidas = []
        escolha = Interface_CLI.mostrar_menu_principal(
            entrada=lambda _: "2",
            saida=saidas.append,
            limpar=lambda: None,
        )

        self.assertEqual(escolha, "2")
        tela = "\n".join(saidas)
        self.assertIn("DRAGONIC 4456 // CONSOLE DE CONTROLE", tela)
        self.assertIn("[1] Inicializar chat local", tela)
        self.assertIn("[3] Desligar Dragonic", tela)


if __name__ == "__main__":
    unittest.main()
