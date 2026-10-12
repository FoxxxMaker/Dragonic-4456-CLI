import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

import Backup_Chat
import Benchmark
import Chat
import Interface_CLI
import MCP_Local


class BackupChatTests(unittest.TestCase):
    def test_salvar_configuracao_persiste_json(self):
        caminho_original = Chat.CAMINHO_CONFIGURACAO
        configuracao_original = Chat.config
        with tempfile.TemporaryDirectory() as diretorio_temporario:
            caminho_temporario = Path(diretorio_temporario) / "Config.json"
            Chat.CAMINHO_CONFIGURACAO = caminho_temporario
            Chat.config = {"temperature": 0.7, "max_tokens": 120}
            try:
                Chat.salvar_configuracao()
                conteudo = json.loads(caminho_temporario.read_text(encoding="utf-8"))
            finally:
                Chat.CAMINHO_CONFIGURACAO = caminho_original
                Chat.config = configuracao_original

        self.assertEqual(conteudo["temperature"], 0.7)
        self.assertEqual(conteudo["max_tokens"], 120)

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

    def test_listar_e_carregar_backup(self):
        with tempfile.TemporaryDirectory() as diretorio_temporario:
            caminho = Backup_Chat.salvar_backup(
                [{"papel": "usuario", "conteudo": "continuar"}],
                "prompt",
                diretorio_temporario,
            )
            backups = Backup_Chat.listar_backups(diretorio_temporario)
            conteudo = Backup_Chat.carregar_backup(caminho)

        self.assertEqual(backups, [caminho])
        self.assertEqual(conteudo["mensagens"][0]["conteudo"], "continuar")

    def test_chat_retoma_historico_e_usa_prompt_original(self):
        configuracao_original = Chat.config
        Chat.config = {**configuracao_original, "backup_chats_habilitado": False}
        entradas = iter(["nova mensagem", "sair"])
        prompts = []

        def modelo(**argumentos):
            prompts.append(argumentos["prompt"])
            return {"choices": [{"text": "continuação"}]}

        saidas = []
        try:
            Chat.chat(
                modelo,
                entrada=lambda _: next(entradas),
                saida=saidas.append,
                historico_inicial=[{"papel": "usuario", "conteudo": "mensagem antiga"}],
                system_prompt="prompt antigo",
            )
        finally:
            Chat.config = configuracao_original

        self.assertIn("prompt antigo", prompts[0])
        self.assertIn("mensagem antiga", prompts[0])
        self.assertIn("CHAT RETOMADO", "\n".join(saidas))
        self.assertIn("Você: mensagem antiga", "\n".join(saidas))


class BenchmarkTests(unittest.TestCase):
    def test_benchmark_retorna_medidas_da_resposta(self):
        resultado = Benchmark.executar(
            lambda **_: {"choices": [{"text": "ok"}], "usage": {"completion_tokens": 3}},
            {"max_tokens": 80, "stop": []},
        )

        self.assertEqual(resultado["tokens"], 3)
        self.assertGreaterEqual(resultado["duracao_segundos"], 0)


class McpLocalTests(unittest.TestCase):
    def test_calculadora_mcp_aceita_operacoes_basicas(self):
        resultado = MCP_Local.chamar_ferramenta("calcular", {"expressao": "2 * (3 + 4)"})

        self.assertFalse(resultado["isError"])
        self.assertEqual(resultado["content"][0]["text"], "Resultado: 14")

    def test_chat_mostra_nome_gguf_e_usa_resultado_mcp(self):
        configuracao_original = Chat.config
        Chat.config = {**configuracao_original, "backup_chats_habilitado": False}
        respostas = iter([
            '<mcp>{"name":"calcular","arguments":{"expressao":"2+2"}}</mcp>',
            "O resultado é 4.",
        ])
        saidas = []

        def modelo(**_):
            return {"choices": [{"text": next(respostas)}]}

        try:
            Chat.chat(
                modelo,
                entrada=lambda _: "sair" if len(saidas) > 1 else "quanto é 2+2?",
                saida=saidas.append,
                nome_modelo="modelo-teste.gguf",
            )
        finally:
            Chat.config = configuracao_original

        self.assertEqual(saidas[0], "modelo-teste.gguf")
        self.assertIn("Model: O resultado é 4.", saidas)


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
        self.assertIn("[3] Visualizar ou continuar chats salvos", tela)
        self.assertIn("[4] Desligar Dragonic", tela)


if __name__ == "__main__":
    unittest.main()
