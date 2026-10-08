from dataclasses import dataclass
from typing import Any

from sqlalchemy.orm import Session

from app.tools.registry import registry


@dataclass
class AgentResponse:
    text: str
    tool_calls: list[dict[str, Any]]


class AgentRuntime:
    """Provider-agnostic agent orchestration boundary.

    The LLM provider decides which tool to call; this runtime owns the
    trusted execution boundary and supplies the database/user context.
    """

    async def execute_tool(
        self,
        db: Session,
        user_id: int,
        name: str,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        tool = registry.get(name)
        if tool.kind.value in {"destructive", "sensitive"}:
            raise PermissionError(f"Tool requires explicit confirmation: {name}")

        return await registry.execute(
            name,
            context={"db": db, "user_id": user_id},
            arguments=arguments,
        )

    async def handle(self, db: Session, user_id: int, message: str) -> AgentResponse:
        # LLM provider + structured tool calling is the next provider-specific layer.
        return AgentResponse(
            text=f"Recebi sua mensagem: {message}",
            tool_calls=[],
        )

    def available_tools(self) -> list[dict[str, Any]]:
        return registry.definitions()


runtime = AgentRuntime()
