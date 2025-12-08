import logging
import azure.functions as func
from ..shared.agent import MCPAgent
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Simple proxy to MCP tool endpoint via MCPAgent
    tool = req.route_params.get('tool') if req.route_params else None
    q = req.params.get('q') if req.params else None
    if not tool:
        return func.HttpResponse(json.dumps({"error": "tool not specified"}), status_code=400, mimetype="application/json")
    agent = MCPAgent()
    res = agent.call_tool(tool, {"q": q})
    return func.HttpResponse(json.dumps(res, ensure_ascii=False), status_code=200, mimetype="application/json")
