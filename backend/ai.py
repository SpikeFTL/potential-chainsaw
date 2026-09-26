import httpx
from .config import DEMO_MODE,NVIDIA_API_KEY,NVIDIA_BASE_URL,NVIDIA_MODEL

def demo_sql(q):
    q=q.lower()
    if "average" in q and "course" in q:
        return "SELECT c.name AS course, ROUND(AVG(m.score),2) AS average_score FROM marks m JOIN courses c ON c.id=m.course_id GROUP BY c.name ORDER BY average_score DESC"
    if "top" in q and "student" in q:
        return "SELECT s.name, ROUND(AVG(m.score),2) AS average_score FROM students s JOIN marks m ON s.id=m.student_id GROUP BY s.name ORDER BY average_score DESC LIMIT 3"
    if "attendance" in q:
        return "SELECT s.name, ROUND(100.0*SUM(a.attended)/SUM(a.total),2) AS attendance_percent FROM students s JOIN attendance a ON s.id=a.student_id GROUP BY s.name ORDER BY attendance_percent DESC"
    if "fee" in q:
        return "SELECT s.name,(f.amount_due-f.amount_paid) AS outstanding FROM students s JOIN fees f ON s.id=f.student_id WHERE f.amount_due>f.amount_paid ORDER BY outstanding DESC"
    return "SELECT name,branch,year FROM students ORDER BY id"

def chat(system,user):
    if not NVIDIA_API_KEY:
        raise RuntimeError("NVIDIA_API_KEY is missing. Set DEMO_MODE=true or add your key.")
    r=httpx.post(f"{NVIDIA_BASE_URL.rstrip('/')}/chat/completions",headers={"Authorization":f"Bearer {NVIDIA_API_KEY}"},json={"model":NVIDIA_MODEL,"messages":[{"role":"system","content":system},{"role":"user","content":user}],"temperature":0},timeout=30)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()

def generate_sql(question,schema):
    if DEMO_MODE:
        return demo_sql(question)
    return chat("Generate ONLY one safe read-only SELECT query. Use only the supplied schema.",f"Schema:\n{schema}\nQuestion:\n{question}").strip()

def explain(question,sql,results):
    if DEMO_MODE:
        return "Demo mode: the question was mapped to a deterministic read-only query so the full application workflow can be demonstrated without an API key."
    return chat("Explain these SQL results in 3 concise factual bullets. Do not invent facts.",f"Question: {question}\nSQL: {sql}\nResults: {results}")
