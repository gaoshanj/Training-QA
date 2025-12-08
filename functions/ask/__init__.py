import json
import os
import logging
import azure.functions as func

from ..shared.agent import MCPAgent

def _generate_answer(question: str) -> dict:
    # Minimal implementation: if Azure OpenAI creds are set, call the service.
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    key = os.environ.get("AZURE_OPENAI_KEY")
    if endpoint and key:
        # Placeholder for real call to Azure OpenAI / Azure AI Language
        # Implement proper client usage here (azure.ai.openai.OpenAIClient)
        logging.info("Would call Azure OpenAI here")
        answer = f"（示例回答）针对：{question} 的简短回答。"
    else:
        answer = f"（本地回显）你问：{question}。请在环境变量中配置 AZURE_OPENAI_* 来启用模型回应。"

    ssml = f"<speak>{answer}</speak>"
    return {"answerText": answer, "ssml": ssml, "meta": {"source": "local-echo"}}

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.get_json() if req.get_body() else {}
    except ValueError:
        data = {}
    q = data.get("question") or req.params.get("q") if req.params else None
    if not q:
        return func.HttpResponse(json.dumps({"error": "missing question"}), status_code=400, mimetype="application/json")

    # Optionally use MCP tools for retrieval
    agent = MCPAgent()
    faq = agent.call_tool("faq", {"q": q})

    answer = _generate_answer(q)
    answer["meta"]["faq"] = faq

    return func.HttpResponse(json.dumps(answer, ensure_ascii=False), status_code=200, mimetype="application/json")
