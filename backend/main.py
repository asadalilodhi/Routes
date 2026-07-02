# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from pydantic import BaseModel
# pyrefly: ignore [missing-import]
import uvicorn
from skills.intent_parser import IntentParsingSkill
from skills.route_optimizer import RouteOptimizationSkill
from agents import ParserAgent, EvaluatorAgent, RouterAgent, UserProxyAgent
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Multi-Agent Errands Optimizer")

# Initialize Skills
intent_parser = IntentParsingSkill()
route_optimizer = RouteOptimizationSkill()

# Initialize Agents
parser_agent = ParserAgent(parser_skill=intent_parser)
evaluator_agent = EvaluatorAgent()
router_agent = RouterAgent(router_skill=route_optimizer)
user_proxy = UserProxyAgent()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    route_details: dict | None = None

@app.get("/")
def read_root():
    return {"status": "Multi-Agent Backend is Running!"}

@app.post("/chat", response_model=ChatResponse)
def handle_chat(request: ChatRequest):
    user_msg = request.message
    
    # --- Multi-Agent Workflow ---
    
    # 1. Parse intent
    parsed_intent = parser_agent.execute(user_msg)
    
    # 2. Evaluate locations and times using MCP Tools
    distance_matrix = evaluator_agent.execute(parsed_intent.get("errands", []))
    
    # 3. Optimize the route
    optimized_route = router_agent.execute(
        start_loc=parsed_intent.get("start_location"),
        end_loc=parsed_intent.get("end_location"),
        errands=parsed_intent.get("errands", []),
        distance_matrix=distance_matrix
    )
    
    # 4. Final user formatting
    final_message = user_proxy.execute(optimized_route)
    
    return ChatResponse(
        response=final_message,
        route_details=optimized_route
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
