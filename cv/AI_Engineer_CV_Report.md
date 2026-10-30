# CV report: AI Engineer

## Files

| File | What it is |
|---|---|
| `Md_Shamiul_Islam_Riyad_AI_Engineer_CV.pdf` | Submission copy. One A4 page, single column, selectable text, clickable links |
| `Md_Shamiul_Islam_Riyad_AI_Engineer_CV.docx` | Editable Word copy (`python3 cv/build_docx.py Md_Shamiul_Islam_Riyad_AI_Engineer_CV`) |
| `Md_Shamiul_Islam_Riyad_AI_Engineer_CV.html` | Source for the PDF (`node cv/build_ai_engineer_cv.cjs`) |

## How the CV maps to the role

| The role asks for | Where the CV shows it |
|---|---|
| Python and LLM API applications | ragkit-dev (Python package), the FastAPI RAG services in FactoryBrain and rag-kit; Gemini, Claude and OpenAI APIs |
| RAG and embeddings | ragkit-dev, rag-kit and FactoryBrain (Qdrant, local BGE-M3 or Gemini embeddings, cited answers) |
| AI agents and automation | FactoryBrain agent runs with human approval, LLM document extraction; Doctor MCP Server tool endpoints; NogorSathi tool-calling demo |
| Prompt engineering | QueueStorm (structured JSON, fallback, safety filter), Chokh (Bengali system prompt), FactoryBrain (schema-constrained extraction) |
| Demos, labs and hands-on exercises | 12 tutorial-style guides in rag-kit, step-by-step modules in ragkit-dev, deployed Chokh demo |
| Explaining AI simply in Bangla and English | Bangla-language products (AI Study Assistant, Chokh, QueueStorm). Your spoken languages aren't listed yet. See the questions below |
| Working with founding teams and mentors | 7 hackathons, team projects (NogorSathi, ShilpoHubBD) |

## Implemented vs explored

Only implemented work is claimed. Checked on 2026-10-30 against fresh clones (default branch).

| Technology | Status | Evidence |
|---|---|---|
| Gemini API | Implemented | `rag_kit/step10_generate.py`, `Chokh.Api/Program.cs`, `AI-Study-Assistant` backend |
| Claude API | Implemented | `sust_preli/.../AnthropicReasoningService.cs`; Anthropic branch in FactoryBrain `LlmVisionDefectProvider.cs` and `ExtractionProviders.cs` |
| OpenAI API | Implemented | OpenAI branch in the same two FactoryBrain providers (`/v1/chat/completions`) |
| Qdrant, LangChain | Implemented | `rag_kit/step06_vector_store.py`, `rag-kit/rag/`, `FactoryBrain/rag/` |
| Embeddings (BGE-M3, Gemini) | Implemented | `rag_kit/step05_embedding.py` |
| FastAPI, Streamlit | Implemented | `rag_kit/api.py`, `rag_kit/ui/app.py`, `FactoryBrain/rag/main.py` |
| pgvector, BM25 hybrid scoring | Written, not live | `FactoryBrain/.../HybridScorer.cs` exists, but Ask now goes through the Python service. Left off this CV |
| Gemma 4 function calling | Designed, mocked | NogorSathi demo replays scripted tool calls. The CV says "demo" |
| MCP | MCP-style HTTP | `make-my-mcp-server` exposes `tools/list` and `tools/call` over Express. It doesn't use the MCP SDK, so the CV says "list and call endpoints" |
| PyTorch, OpenCV | Exploring | Mango classifier returns a fixed prediction; no trained model. Listed under "Currently learning" |

## Evidence for each claim

| Claim | Evidence |
|---|---|
| FactoryBrain: RAG service answers from retrieved chunks, page citations | `Infrastructure/Services/AskService.cs` → `Rag/PyRagClient.cs` → `rag/main.py` `/api/kb/{collection}/query`; `BuildCitations` titles include the page |
| FactoryBrain: agents ground fixes on live data, risky runs need approval | `AgentRunService.cs`: `ReadContextAsync` (lines below target, machines down or at risk), `BuildQuestion`, `approvalPending = risk != RiskTier.Low` |
| FactoryBrain: schema-constrained extraction, quotes checked | `Infrastructure/Merchandising/ExtractionProviders.cs` (`LlmDocumentExtractionProvider`: "its quotes are then checked against the document text") |
| FactoryBrain: vision defect detection, switchable provider | `Qc/LlmVisionDefectProvider.cs` (JSON with `box_2d`; `openai`, `anthropic`, `gemini` cases) |
| FactoryBrain: 240+ tests | 174 `[Fact]`/`[Theory]`, 57 Playwright `test(`, 11 pytest `def test_` |
| ragkit-dev: 11 modules, context-only answers, per-claim citations | `src/rag_kit/step01…step11`; `step10_generate.py` prompt ("tag every claim with the [S1]..[Sn] marker") |
| ragkit-dev: CLI, FastAPI, Streamlit, npm generator, 290+ offline tests | `cli.py`, `api.py`, `ui/app.py`, `generator/`; 217 pytest + 75 Node tests; `ci.yml` guard step |
| rag-kit: .NET gateway, plan limits, Qdrant per knowledge base | `rag-kit/README.md` (gateway, per-KB collections, plan limits), `Integrations/PythonRag/` |
| rag-kit: 12 tutorial-style guides | `rag-kit/docs/` (12 guides plus an index; each answers what, why, how, where, how to change, example) |
| QueueStorm, Chokh, NogorSathi, AI Study Assistant | Same evidence as `BIAI_CV_Report.md` |
| Doctor MCP Server: 5 tools, MySQL, Zod | `src/constants/tools.js`, `src/db/pool.js`, `src/validators/doctorScheduleValidators.js` |
| ShilpoHubBD numbers | From the verified `Webmotech_CV_Report.md` |
| Achievements and ratings | From your profile README. Ratings change, so check them before sending |

## Left out on purpose

- **Mango Fraud Detection** (placeholder model), **Smart Shelf Robot** (1 of 43 commits) and **Nurture-Glow** (fork, 4 of 48 commits).
- **Most of the NogorSathi repository.** It is the unrelated VoiceAI-Asuna codebase, added in one commit.
- **The research proposals and slides in this repository.** They were drafted by Claude.
- **Phone number, CGPA, location and spoken languages.** They aren't in your profile or earlier CVs.
