from __future__ import annotations
from uuid import UUID
from sqlalchemy.orm import Session
from context.tool_context import ToolContext
from core.models.dataset import Dataset
from core.models.user import User
from providers.provider_factory import ProviderFactory
from services.ai.conversation_memory_service import ConversationMemoryService
from services.ai.prompt_service import PromptService
from services.chat_message_service import ChatMessageService
from services.chat_service import ChatService
from services.search.retrieval_service import RetrievalService
from services.subscription.quota_service import QuotaService
from services.usage_service import UsageService
from tools.executor import ToolExecutor
from tools.registry import tool_registry

class AIService:

    def __init__(self, db: Session, provider: str = "openai") -> None:
        self.db = db

        self.provider = ProviderFactory.get(provider)
        self.chat = ChatService(db)
        self.messages = ChatMessageService(db)
        self.memory = ConversationMemoryService(db)
        self.prompt = PromptService(db)
        self.retrieval = RetrievalService(db)
        self.quota = QuotaService(db)
        self.usage = UsageService(db)
        self.executor = ToolExecutor()

    async def chat(self, *, user: User, dataset: Dataset, question: str, session_id: UUID | None = None) -> dict:
        session = self._resolve_session( dataset=dataset, user=user, session_id=session_id)
        self._check_usage(tenant_id=dataset.tenant_id)
        self._save_user_message(session=session, user=user, question=question)
        retrieved_context = await self._retrieve_context(dataset=dataset, question=question)
        messages = self.prompt.build( chat_session_id=session.id, retrieved_context=retrieved_context, user_message=question)

        response = await self._execute_model(session=session,dataset=dataset,user=user,messages=messages)

        self._save_assistant_message(
            session=session,
            response=response,
        )

        self._record_usage(
            tenant_id=dataset.tenant_id,
            response=response,
        )

        return response

    def _resolve_session( self, *, dataset: Dataset, user: User, session_id: UUID | None):
        if session_id:
            return self.chat.get(session_id)

        session = self.chat.latest(dataset.id)

        if session:
            return session

        return self.chat.create(actor_id=user.id, dataset=dataset, title=None)

    def _check_usage(self, *, tenant_id: UUID) -> None:
        usage = self.usage.get(tenant_id)

        self.quota.require_chat(tenant_id=tenant_id, current_usage=usage.chat_messages_used)

    def _save_user_message(self, *, session, user: User, question: str):

        self.messages.add_user(actor_id=user.id, session=session, content=question)

    async def _retrieve_context(self, *, dataset: Dataset, question: str):

        return await self.retrieval.retrieve( dataset_id=dataset.id, question=question, limit=8)

    async def _execute_model(self, *, session, dataset, user, messages):

        context = ToolContext( db=self.db, user=user, dataset=dataset, session=session, memory=self.memory, runtime={})

        response = await self.provider.chat( messages=messages, tools=tool_registry.metadata())

        if response.tool_calls:
            return await self.executor.run(provider=self.provider, response=response, messages=messages, context=context)

        return {
            "provider": response.provider,
            "model": response.model,
            "message": response.content,
            "tool_calls": [],
            "usage": {
                "prompt_tokens": response.prompt_tokens,
                "completion_tokens": response.completion_tokens,
                "total_tokens": response.total_tokens,
            },
        }

    def _save_assistant_message(self, *, session, response: dict):

        self.messages.add_assistant(
            actor_id=session.created_by,
            session=session,
            content=response["message"],
            provider=response["provider"],
            model=response["model"],
            prompt_tokens=response["usage"]["prompt_tokens"],
            completion_tokens=response["usage"]["completion_tokens"],
            total_tokens=response["usage"]["total_tokens"],
        )

    def _record_usage(self, *, tenant_id: UUID, response: dict):
        usage = response["usage"]

        self.usage.record_chat_message(tenant_id=tenant_id)

        self.usage.record_ai_usage(tenant_id=tenant_id, prompt_tokens=usage["prompt_tokens"], completion_tokens=usage["completion_tokens"])