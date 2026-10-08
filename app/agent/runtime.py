from dataclasses import dataclass
from typing import Any

from app.tools.registry import registry


@dataclass
class AgentResponse:
    text: str
    tool_calls: list[dict[str, Any]]


class AgentRuntime:
    """Provider-agnostic orchestration boundary for the LLM."""

    async def handle(self, user_id: int, message: str) -> AgentResponse:
        # The LLM provider will be wired here. Keeping orchestration separate
        # makes tool execution and safety policies independent from the provider.
        return AgentResponse(
            text=f"Recebi sua mensagem: {message}",
            tool_calls=[],
        )

    def available_tools(self) -> list[dict[str, Any]]:
        return registry.definitions()
