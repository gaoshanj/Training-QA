import os
import requests
import logging

class MCPAgent:
    """A minimal MCP agent wrapper for calling tool endpoints.

    This is a lightweight placeholder: replace with a proper MCP client when available.
    """
    def __init__(self, endpoint: str | None = None, timeout: int = 10):
        self.endpoint = endpoint or os.environ.get("MCP_TOOL_ENDPOINT")
        self.timeout = timeout

    def call_tool(self, tool_name: str, params: dict | None = None) -> dict:
        if not self.endpoint:
            logging.warning("MCP endpoint not configured")
            return {"error": "MCP endpoint not configured"}
        url = f"{self.endpoint.rstrip('/')}/tools/{tool_name}"
        try:
            resp = requests.get(url, params=params or {}, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logging.exception("MCP tool call failed")
            return {"error": str(e)}
