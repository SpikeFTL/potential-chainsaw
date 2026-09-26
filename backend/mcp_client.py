import asyncio,json,sys
from contextlib import AsyncExitStack
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
from .config import MCP_SERVER_PATH

class MCPClient:
    async def call_async(self,tool,args=None):
        params=StdioServerParameters(command=sys.executable,args=["-m","mcp_server.server"])
        async with AsyncExitStack() as stack:
            read,write=await stack.enter_async_context(stdio_client(params))
            session=await stack.enter_async_context(ClientSession(read,write))
            await session.initialize()
            result=await session.call_tool(tool,arguments=args or {})
            if getattr(result,"structuredContent",None):
                return result.structuredContent
            if getattr(result,"structured_content",None):
                return result.structured_content
            for item in getattr(result,"content",[]):
                if getattr(item,"text",None):
                    return json.loads(item.text)
            raise RuntimeError("MCP returned no structured result")

    def call(self,tool,args=None):
        return asyncio.run(self.call_async(tool,args))
