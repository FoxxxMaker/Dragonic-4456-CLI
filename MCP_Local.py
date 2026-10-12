"""Núcleo MCP local inicial: ferramentas seguras para o chat."""

import ast
import json
import re
from datetime import datetime


PADRAO_CHAMADA = re.compile(r"<mcp>\s*(\{.*?\})\s*</mcp>", re.DOTALL)


def listar_ferramentas():
    """Expõe uma lista no formato de ferramentas MCP para futuras integrações."""
    return [
        {
            "name": "hora_atual",
            "description": "Informa a data e a hora locais.",
            "inputSchema": {"type": "object", "properties": {}},
        },
        {
            "name": "calcular",
            "description": "Calcula uma expressão matemática simples.",
            "inputSchema": {
                "type": "object",
                "properties": {"expressao": {"type": "string"}},
                "required": ["expressao"],
            },
        },
    ]


def _calcular(expressao):
    arvore = ast.parse(expressao, mode="eval")

    def avaliar(no):
        if isinstance(no, ast.Expression):
            return avaliar(no.body)
        if isinstance(no, ast.Constant) and isinstance(no.value, (int, float)):
            return no.value
        if isinstance(no, ast.UnaryOp) and isinstance(no.op, (ast.UAdd, ast.USub)):
            return (+1 if isinstance(no.op, ast.UAdd) else -1) * avaliar(no.operand)
        if isinstance(no, ast.BinOp) and isinstance(no.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod)):
            operadores = {
                ast.Add: lambda a, b: a + b,
                ast.Sub: lambda a, b: a - b,
                ast.Mult: lambda a, b: a * b,
                ast.Div: lambda a, b: a / b,
                ast.Pow: lambda a, b: a**b,
                ast.Mod: lambda a, b: a % b,
            }
            return operadores[type(no.op)](avaliar(no.left), avaliar(no.right))
        raise ValueError("A expressão aceita apenas números e operações matemáticas básicas.")

    return avaliar(arvore)


def chamar_ferramenta(nome, argumentos):
    """Executa uma ferramenta e devolve uma resposta inspirada em tools/call."""
    try:
        if nome == "hora_atual":
            texto = datetime.now().strftime("Data e hora local: %d/%m/%Y %H:%M:%S")
        elif nome == "calcular":
            texto = f"Resultado: {_calcular(argumentos['expressao'])}"
        else:
            raise ValueError(f"Ferramenta MCP desconhecida: {nome}")
        return {"content": [{"type": "text", "text": texto}], "isError": False}
    except (KeyError, SyntaxError, ValueError, ZeroDivisionError) as erro:
        return {"content": [{"type": "text", "text": f"Erro MCP: {erro}"}], "isError": True}


def extrair_chamada(texto):
    """Lê uma chamada emitida pelo modelo no formato <mcp>{...}</mcp>."""
    encontrado = PADRAO_CHAMADA.search(texto)
    if not encontrado:
        return None
    try:
        chamada = json.loads(encontrado.group(1))
        return chamada["name"], chamada.get("arguments", {})
    except (json.JSONDecodeError, KeyError, TypeError):
        return None


def instrucao_para_modelo():
    ferramentas = ", ".join(ferramenta["name"] for ferramenta in listar_ferramentas())
    return (
        "\n\nFerramentas MCP locais disponíveis: " + ferramentas + ". "
        "Quando precisar de uma, responda somente com "
        '<mcp>{"name":"nome_da_ferramenta","arguments":{}}</mcp>. '
        "Você receberá o resultado para então responder ao usuário."
    )
