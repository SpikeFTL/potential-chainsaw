# SQLMind Architecture

SQLMind is divided into three runtime layers.

1. Frontend: React/Vite provides Ask, Smart Analysis, Dashboard and schema inspection.
2. SQLMind-Agent backend: FastAPI receives requests, obtains schema through the MCP client, generates or selects read-only SQL, validates it, executes it through MCP, and returns structured results.
3. SQLMind-MCP: the MCP server exposes database tools for table listing, schema discovery, table description and safe SELECT execution.

End-to-end flow:

User -> React -> FastAPI -> MCP schema -> NIM/demo SQL generation -> safety validation -> MCP -> SQLite -> results -> React.

The separation keeps the database tool layer reusable independently of the UI and AI layer.
