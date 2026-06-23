import os
import time
from fastapi import FastAPI
from pydantic import BaseModel, validator
from backend_logic.brain import QuantAgent

ucrt64_bin_path = r"C:\msys64\ucrt64\bin"
if hasattr(os, 'add_dll_directory'):
    os.add_dll_directory(ucrt64_bin_path)

import backend_logic.hedge_core as hedge_core

app = FastAPI(title="Hedge-Mind Quant API")
agent = QuantAgent() # start brain

class SimulationRequest(BaseModel):
    asset_price: float
    risk_free_rate: float
    volatility: float
    time_horizon: float
    paths: int = 1_000_000

    @validator('risk_free_rate', 'volatility')
    def convert_to_decimal(cls, value):
        if value >= 1.0: return value / 100.0
        return value

class ChatRequest(BaseModel):
    query: str


@app.post("/api/v1/simulate")
async def run_monte_carlo(req: SimulationRequest):
    """Direct JSON access to the C++ Engine"""
    start_time = time.time()
    engine = hedge_core.SimulationEngine(
        req.asset_price, req.risk_free_rate, req.volatility, req.time_horizon, req.paths
    )
    results = engine.run_simulation_matrix()
    expected_price = engine.calculate_expected_value(results)
    
    return {
        "status": "success",
        "expected_price": round(expected_price, 4),
        "execution_time_seconds": round(time.time() - start_time, 4),
        "parameters": req.model_dump()
    }

@app.post("/api/v1/chat")
async def chat_to_simulate(req: ChatRequest):
    """Natural Language access to the C++ Engine via AI Orchestration"""
    
    extracted_params = agent.parse_query(req.query)
    
    sim_request = SimulationRequest(
        asset_price=extracted_params.asset_price,
        risk_free_rate=extracted_params.risk_free_rate,
        volatility=extracted_params.volatility,
        time_horizon=extracted_params.time_horizon,
        paths=1_000_000
    )
    return await run_monte_carlo(sim_request)

    # uvicorn server:app --reload : command to run the uvicorn server