from mcp.server.fastmcp import FastMCP
from mcp_server.database import Database

mcp=FastMCP("SQLMind MCP Server")
db=Database()

@mcp.tool()
def list_tables():
    return {"success":True,"tables":[t["name"] for t in db.schema()]}

@mcp.tool()
def get_database_schema():
    return {"success":True,"schema":{t["name"]:t["columns"] for t in db.schema()}}

@mcp.tool()
def describe_table(table_name:str):
    for t in db.schema():
        if t["name"]==table_name:
            return {"success":True,"table":t["name"],"columns":t["columns"]}
    return {"success":False,"error":"Requested table does not exist."}

@mcp.tool()
def run_select_query(sql:str):
    return db.query(sql)

if __name__=="__main__":
    mcp.run()
