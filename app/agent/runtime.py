import json
from dataclasses import dataclass
from typing import Any

from openai import AsyncOpenAI
from sqlalchemy.orm import Session

from app.agent.context import make_agent_context
from app.config import settings
from app.tools.registry import registry
import app.tools  # noqa: F401,E402


@dataclass
class AgentResponse:
    text: str
    tool_calls: list[dict[str, Any]]


class AgentRuntime:
    """LLM orchestration with a trusted backend tool-execution boundary."""

    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key=settings.llm_api_key) if settings.llm_api_key else None

    def available_tools(self) -> list[dict[str, Any]]:
        return registry.definitions()

    async def execute_tool(self, db: Session, user_id: int, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        tool = registry.get(name)
        if tool.kind.value in {"destructive", "sensitive"}:
            raise PermissionError(f"Tool requires explicit confirmation: {name}")
        return await registry.execute(name, context={"db": db, "user_id": user_id}, arguments=arguments)

    async def handle(self, db: Session, user_id: int, message: str) -> AgentResponse:
        if not self.client:
            return AgentResponse("LLM_API_KEY não configurada.", [])

        context = make_agent_context(db, user_id, message)
        tools = [{
            "type": "function",
            "function": {
                "name": item["name"],
                "description": item["description"],
                "parameters": item["input_schema"],
            },
        } for item in self.available_tools()]

        messages: list[dict[str, Any]] = [{
            "role": "system",
            "content": (
                "Você é o Flash, um copiloto pessoal via WhatsApp. "
                "Se uma ferramenta for necessária, use-a; nunca diga que executou "
                "uma ação sem receber o resultado real da ferramenta. "
                "Se faltar data/hora para um lembrete, peça esclarecimento."
            ),
        }]
        messages.append({"role": "system", "content": "Contexto: " + json.dumps(context, ensure_ascii=False, default=str)})
        messages.append({"role": "user", "content": message})

        first = await self.client.chat.completions.create(
            model=settings.llm_model,
            messages=messages,
            tools=tools or None,
            tool_choice="auto" if tools else None,
        )

        choice = first.choices[0]
        if not choice.message.tool_calls:
            return AgentResponse(choice.message.content or "", [])

        tool_results: list[dict[str, Any]] = []
        for call in choice.message.tool_calls:
            arguments = json.loads(call.function.arguments or "{}")
            try:
                result = await self.execute_tool(db, user_id, call.function.name, arguments)
            except Exception as exc:
                result = {"status": "error", "message": str(exc)}
            tool_results.append({
                "tool_call_id": call.id,
                "name": call.function.name,
                "result": result,
            })

        followup_messages = list(messages)
        followup_messages.append(choice.message.model_dump(exclude_none=True))
        for item in tool_results:
            followup_messages.append({
                "role": "tool",
                "tool_call_id": item["tool_call_id"],
                "content": json.dumps(item["result"], ensure_ascii=False, default=str),
            })

        final = await self.client.chat.completions.create(
            model=settings.llm_model,
            messages=followup_messages,
            tools=tools or None,
            tool_choice="none",
        )
        return AgentResponse(final.choices[0].message.content or "", tool_results)


runtime = AgentRuntime()
