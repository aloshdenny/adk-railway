import os
import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from agent import orchestrator

from dotenv import load_dotenv
load_dotenv()

# ── App setup ────────────────────────────────────────────
app = FastAPI(title="Calculator Multi-Agent")

session_service = InMemorySessionService()
APP_NAME = "calculator_app"

runner = Runner(
    agent=orchestrator,
    app_name=APP_NAME,
    session_service=session_service,
)

# ── Request schema ────────────────────────────────────────
class QueryRequest(BaseModel):
    query: str
    user_id: str = "user_1"
    session_id: str = "session_1"

# ── Helper ────────────────────────────────────────────────
async def run_agent(query: str, user_id: str, session_id: str) -> str:
    # Create session if it doesn't exist
    try:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id
        )
    except Exception:
        pass  # Session already exists

    content = types.Content(
        role="user",
        parts=[types.Part(text=query)]
    )

    final_response = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text

    return final_response

# ── Routes ────────────────────────────────────────────────
@app.get("/")
async def root():
    return {"status": "ok", "agent": "Calculator Multi-Agent"}

@app.post("/ask")
async def ask(request: QueryRequest):
    response = await run_agent(request.query, request.user_id, request.session_id)
    return JSONResponse({"query": request.query, "response": response})

# ── Entry point ───────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
