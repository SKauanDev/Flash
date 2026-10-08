from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Awaitable, Callable


class ToolKind(StrEnum):
    READ = "read"
    WRITE = "write"
    DESTRUCTIVE = "destructive"
    SENSITIVE = "sensitive"


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    kind: ToolKind
    schema: dict[str, Any]
    executor: Callable[..., Awaitable[dict[str, Any]]]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        return self._tools[name]

    def definitions(self) -> list[dict[str, Any]]:
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "kind": tool.kind.value,
                "input_schema": tool.schema,
            }
            for tool in self._tools.values()
        ]


registry = ToolRegistry()
