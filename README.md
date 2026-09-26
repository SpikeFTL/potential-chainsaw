# SQLMind

An AI-assisted, read-only SQL analytics application for natural-language database exploration.

## What it does

SQLMind lets a user ask a database question in plain English, such as:

> Show the average score by course.

The application:

1. Reads the connected database schema through SQLMind-MCP.
2. Uses NVIDIA NIM / Llama 3.1 8B Instruct to generate a read-only SQL query.
3. Validates the generated SQL before execution.
4. Sends the query to SQLMind-MCP over MCP/stdio.
5. Executes the query against SQLite, MySQL, or PostgreSQL.
6. Returns rows, generated SQL, a chart-ready result, and an AI explanation.
7. Supports Smart Analysis, dashboard generation, CSV export, and Excel export.

## Architecture

```text
React + Vite frontend
        |
        | HTTP/JSON
        v
FastAPI backend (SQLMind-Agent)
        |
        +---- NVIDIA NIM / Llama 3.1 8B
        |
        +---- Read-only SQL safety validation
        |
        v
MCP client  ---- stdio ---->  SQLMind-MCP
                                   |
                          +--------+--------+
                          |        |        |
                       SQLite   MySQL   PostgreSQL
```

## Repository layout

```text
SQLMind/
├── backend/                  # FastAPI application
├── mcp_server/               # MCP database server
├── frontend/                 # React + Vite UI
├── scripts/                  # Demo database setup
├── tests/                    # Backend safety/database tests
├── docs/                     # Architecture notes
├── .env.example
├── requirements.txt
└── README.md
```

## Quick start (Windows PowerShell)

### 1. Backend

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python scripts/init_demo_db.py
python -m uvicorn backend.api:app --reload --port 8001
```

### 2. Frontend

Open a second PowerShell window:

```powershell
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite, usually http://localhost:5173.

### 3. AI mode

Add your NVIDIA API key to .env:

```text
NVIDIA_API_KEY=your_key_here
DEMO_MODE=false
```

Without an API key, keep DEMO_MODE=true. The UI remains fully testable using deterministic demo responses.

## Demo database

The initializer creates:

- students
- courses
- marks
- attendance
- fees

Useful demo questions:

- Show all students.
- Show average score by course.
- Show the top 3 students by score.
- Show attendance by course.
- Show unpaid fees.
- Create a student performance dashboard.
- Analyze student performance.

## Safety

Only read-only SQL is allowed. Queries containing destructive operations such as DROP, DELETE, UPDATE, INSERT, ALTER, TRUNCATE, CREATE, REPLACE, ATTACH, DETACH, VACUUM, or PRAGMA are rejected. Multi-statement chaining is also rejected.

The database layer opens SQLite in read-only mode and caps returned rows.

## Test

```powershell
pytest -q
```

## Notes

This is a single-repository presentation of the SQLMind architecture. The application layer and MCP database layer remain separate modules so that the MCP server can be reused by other AI clients.