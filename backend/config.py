import os
from dotenv import load_dotenv
load_dotenv()
DEMO_MODE=os.getenv("DEMO_MODE","true").lower()=="true"
NVIDIA_API_KEY=os.getenv("NVIDIA_API_KEY")
NVIDIA_BASE_URL=os.getenv("NVIDIA_BASE_URL","https://integrate.api.nvidia.com/v1")
NVIDIA_MODEL=os.getenv("NVIDIA_MODEL","meta/llama-3.1-8b-instruct")
MCP_SERVER_PATH=os.getenv("MCP_SERVER_PATH","mcp_server/server.py")
