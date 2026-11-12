import os


def setup_tracing() -> None:
    """LangSmith se activa solo con las variables de entorno.

    Phoenix se registra si PHOENIX_ENABLED=1 y el colector está levantado.
    """
    if os.getenv("PHOENIX_ENABLED", "0") != "1":
        return
    from phoenix.otel import register

    register(
        project_name=os.getenv("PHOENIX_PROJECT", "api-orquestador"),
        endpoint=os.getenv("PHOENIX_COLLECTOR_ENDPOINT", "http://localhost:6006/v1/traces"),
        auto_instrument=True,
    )
