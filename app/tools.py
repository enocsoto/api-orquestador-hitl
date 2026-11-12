import json
import re

from langchain_core.tools import tool

PEDIDOS: dict[int, dict] = {
    7: {"pedidos": 2, "total": 800},
    102: {"pedidos": 3, "total": 14500},
}
UMBRAL_CRITICO = 10000


@tool
def buscar_fuente(cliente_id: int) -> str:
    """Busca en la base interna cuántos pedidos tuvo un cliente y el total.

    No calcula promedios. Si el cliente no existe, devuelve un error.
    """
    fila = PEDIDOS.get(cliente_id)
    if fila is None:
        return json.dumps(
            {"error": "Cliente no encontrado", "cliente_id": cliente_id},
            ensure_ascii=False,
        )
    return json.dumps({"cliente_id": cliente_id, **fila}, ensure_ascii=False)


@tool
def calcular_ticket_promedio(total: float, cantidad: int) -> str:
    """Calcula el ticket promedio y dice si supera 4000.

    Si cantidad es menor que 1, devuelve un error para que no se invente el número.
    """
    if cantidad < 1 or total < 0:
        return json.dumps(
            {"error": "Datos insuficientes", "sugerencia": "Hace falta total y cantidad."},
            ensure_ascii=False,
        )
    promedio = round(total / cantidad, 2)
    return json.dumps(
        {
            "total": total,
            "cantidad": cantidad,
            "ticket_promedio": promedio,
            "supera_4000": promedio > 4000,
        },
        ensure_ascii=False,
    )


def cliente_de(query: str) -> int | None:
    match = re.search(r"cliente\s+(\d+)", query, flags=re.IGNORECASE)
    if match:
        return int(match.group(1))
    match = re.search(r"\b(\d+)\b", query)
    return int(match.group(1)) if match else None
