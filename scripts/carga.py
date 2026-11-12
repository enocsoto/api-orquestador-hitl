import asyncio
import os
import time

import httpx

API = os.getenv("API_URL", "http://localhost:8000")
CONSULTA = (
    "Investigá cuántos pedidos tuvo el cliente {cliente} y el total, "
    "y decime si el ticket promedio supera 4000."
)


async def main() -> None:
    clientes = [7, 102, 7, 102, 7]
    async with httpx.AsyncClient(timeout=10) as client:
        inicio = time.perf_counter()
        respuestas = await asyncio.gather(
            *[
                client.post(f"{API}/tasks", json={"query": CONSULTA.format(cliente=cliente)})
                for cliente in clientes
            ]
        )
    demora = time.perf_counter() - inicio
    for respuesta in respuestas:
        print(respuesta.status_code, respuesta.json())
    print(f"5 POST en {demora:.3f}s")


if __name__ == "__main__":
    asyncio.run(main())
