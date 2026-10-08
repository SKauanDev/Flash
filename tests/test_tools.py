from app.tools.registry import ToolKind, ToolRegistry


async def fake_executor(**kwargs):
    return kwargs


def test_registry() -> None:
    registry = ToolRegistry()
    registry.register(
        __import__("app.tools.registry", fromlist=["Tool"]).Tool(
            name="test.read",
            description="test",
            kind=ToolKind.READ,
            schema={"type": "object"},
            executor=fake_executor,
        )
    )
    assert registry.get("test.read").kind == ToolKind.READ
    assert registry.definitions()[0]["name"] == "test.read"
