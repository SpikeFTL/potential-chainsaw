from pydantic import BaseModel
from typing import Any

class QueryRequest(BaseModel):
    sql:str
    limit:int=50

class AskRequest(BaseModel):
    question:str
    limit:int=50

class QueryResults(BaseModel):
    columns:list[str]
    rows:list[dict[str,Any]]
    row_count:int
    truncated:bool=False

class AskResponse(BaseModel):
    question:str
    sql:str
    results:QueryResults
    explanation:str

class SchemaResponse(BaseModel):
    tables:list[dict[str,Any]]

class AnalysisRequest(BaseModel):
    question:str
    limit:int=50

class DashboardRequest(BaseModel):
    prompt:str
    limit:int=50
