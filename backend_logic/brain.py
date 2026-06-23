import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
load_dotenv()

class ExtractedSimulationParams(BaseModel):
    asset_price: float = Field(description="The current or starting price of the asset. Default to 100.0 if not stated.")
    risk_free_rate: float = Field(description="The risk-free interest rate as a decimal (e.g., 5% is 0.05). Default to 0.05.")
    volatility: float = Field(description="The implied volatility as a decimal (e.g., 20% is 0.20). Default to 0.20.")
    time_horizon: float = Field(description="The time horizon in years (e.g., 6 months is 0.5). Default to 1.0.")

class QuantAgent:
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.0)
        self.structured_llm = self.llm.with_structured_output(ExtractedSimulationParams)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an elite quantitative finance extraction algorithm. "
                       "Your job is to read user queries about risk scenarios and extract the mathematical parameters. "
                       "Convert all percentages to decimals. Convert all timeframes to years (e.g., 6 months = 0.5). "
                       "If a parameter is missing, use the default values."),
            ("human", "{query}")
        ])
        
        self.pipeline = self.prompt | self.structured_llm

    def parse_query(self, user_query: str) -> ExtractedSimulationParams:
        return self.pipeline.invoke({"query": user_query})