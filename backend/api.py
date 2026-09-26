from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import *
from .safety import *
from .mcp_client import MCPClient
from .ai import generate_sql,explain

app=FastAPI(title="SQLMind",version="1.0")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],allow_methods=["*"],allow_headers=["*"])
mcp=MCPClient()

def normalize(p):
    cols=p.get("columns",[])
    return QueryResults(columns=cols,rows=[dict(zip(cols,r)) for r in p.get("rows",[])],row_count=p.get("row_count",0),truncated=p.get("truncated",False))

@app.get("/health")
def health():
    return {"status":"ok","service":"SQLMind"}

@app.get("/schema",response_model=SchemaResponse)
def schema():
    try:
        p=mcp.call("get_database_schema")
        return SchemaResponse(tables=[{"name":k,"columns":v} for k,v in p.get("schema",{}).items()])
    except Exception as e:
        raise HTTPException(503,str(e))

@app.post("/query",response_model=AskResponse)
def query(req:QueryRequest):
    try:
        sql=add_limit(validate_sql(req.sql),req.limit)
        p=mcp.call("run_select_query",{"sql":sql})
        if not p.get("success"):
            raise HTTPException(400,p.get("error","Query failed"))
        r=normalize(p)
        return AskResponse(question=req.sql,sql=sql,results=r,explanation="Executed a safe read-only SQL query.")
    except UnsafeQueryError as e:
        raise HTTPException(400,str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(503,str(e))

@app.post("/ask",response_model=AskResponse)
def ask(req:AskRequest):
    try:
        q=validate_prompt(req.question)
        sch=schema()
        sql=add_limit(validate_sql(generate_sql(q,sch.model_dump())),req.limit)
        p=mcp.call("run_select_query",{"sql":sql})
        if not p.get("success"):
            raise HTTPException(400,p.get("error","Query failed"))
        r=normalize(p)
        return AskResponse(question=q,sql=sql,results=r,explanation=explain(q,sql,r.model_dump()))
    except UnsafeQueryError as e:
        raise HTTPException(400,str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(503,str(e))

@app.post("/analyze")
def analyze(req:AnalysisRequest):
    specs=[
        ("Average score by course","SELECT c.name AS course,ROUND(AVG(m.score),2) AS average_score FROM marks m JOIN courses c ON c.id=m.course_id GROUP BY c.name ORDER BY average_score DESC"),
        ("Attendance by student","SELECT s.name,ROUND(100.0*SUM(a.attended)/SUM(a.total),2) AS attendance_percent FROM students s JOIN attendance a ON s.id=a.student_id GROUP BY s.name ORDER BY attendance_percent DESC"),
        ("Outstanding fees","SELECT s.name,(f.amount_due-f.amount_paid) AS outstanding FROM students s JOIN fees f ON s.id=f.student_id WHERE f.amount_due>f.amount_paid ORDER BY outstanding DESC")
    ]
    out=[]
    for title,sql in specs:
        p=mcp.call("run_select_query",{"sql":sql})
        out.append({"step":title,"sql":sql,"results":normalize(p).model_dump()})
    return {"question":req.question,"steps":out,"insight":"The analysis combines academic performance, attendance and fee status using read-only SQL."}

@app.post("/dashboard")
def dashboard(req:DashboardRequest):
    specs=[
        ("Total Students","SELECT COUNT(*) AS total_students FROM students"),
        ("Average Score","SELECT ROUND(AVG(score),2) AS average_score FROM marks"),
        ("Average Attendance","SELECT ROUND(100.0*SUM(attended)/SUM(total),2) AS average_attendance FROM attendance"),
        ("Scores by Course","SELECT c.name AS course,ROUND(AVG(m.score),2) AS average_score FROM marks m JOIN courses c ON c.id=m.course_id GROUP BY c.name ORDER BY average_score DESC")
    ]
    widgets=[]
    for title,sql in specs:
        p=mcp.call("run_select_query",{"sql":sql})
        widgets.append({"title":title,"sql":sql,"results":normalize(p).model_dump()})
    return {"title":req.prompt,"widgets":widgets,"insight":"Dashboard generated from the demo academic database using safe read-only queries."}
