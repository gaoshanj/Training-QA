# 培训课程 QA 生成式 Agent（Python + Azure Functions + 静态前端）

说明：这是一个最小可运行的骨架，实现了 Azure Functions（Python）与静态前端（wavesurfer.js）集成，演示文字回复与 TTS 波形播放流程。

快速开始

1. 克隆仓库并进入目录

```powershell
cd "d:/OneDrive - gs82/Code/Training-QA"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. 本地运行 Azure Functions（需要安装 Azure Functions Core Tools）

```powershell
func start
```

3. 运行前端静态站点（在另一个终端）

```powershell
npx live-server frontend --port=8080
```

环境变量

请在 `local.settings.json` 或环境变量中设置：
- `AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_KEY`
- `AZURE_SPEECH_KEY`, `AZURE_SPEECH_REGION`
- `MCP_TOOL_ENDPOINT`（可选）

架构（Mermaid）

```mermaid
flowchart LR
  A[Frontend SPA] -->|HTTPS| B[Azure Functions]
  B --> C[Azure OpenAI / Azure AI Search]
  B --> D[Azure Speech (TTS)]
  B --> E[MCP Tools / Knowledge Sources]
```

后续工作

- 补充 RAG 检索、Key Vault 集成、GitHub Actions 部署脚本（Bicep/Terraform）。
