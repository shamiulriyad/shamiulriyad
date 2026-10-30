# CV report: BIAI Applied AI Internship / Trainee Program

## Files

| File | What it is |
|---|---|
| `Md_Shamiul_Islam_Riyad_BIAI_Applied_AI_Intern_CV.pdf` | Submission copy. One A4 page, single column, selectable text, clickable links |
| `Md_Shamiul_Islam_Riyad_BIAI_Applied_AI_Intern_CV.docx` | Editable Word copy (`python3 cv/build_docx.py Md_Shamiul_Islam_Riyad_BIAI_Applied_AI_Intern_CV`) |
| `Md_Shamiul_Islam_Riyad_BIAI_Applied_AI_Intern_CV.html` | Source for the PDF (`node cv/build_biai_cv.cjs`) |

## How the CV maps to the role

| BIAI asks for | Where the CV shows it |
|---|---|
| Building AI demos | Chokh (deployed), NogorSathi demo, QueueStorm, FactoryBrain demo mode |
| Learning content and tutorials | ragkit-dev: pipeline split into readable step modules, documented step by step, setup generator for new users |
| Testing AI tools | 290+ offline tests in ragkit-dev, 174 xUnit + 57 Playwright in FactoryBrain, LLM fallback, schema validation and safety filter in QueueStorm |
| Working with senior builders and mentors | 7 hackathons, team projects (NogorSathi, ShilpoHubBD: 96 merged pull requests) |
| Research briefs, workshops, student operations | No evidence found in your repositories, so nothing is claimed. See the questions below |

## Evidence for each claim

Checked on 2026-10-30 against fresh clones of each repository (default branch).

| Claim | Evidence |
|---|---|
| ragkit-dev: 11 step modules, cites chunk and PDF page | `rag-learning/src/rag_kit/step01_…step11_*.py`, `step11_answer.py` |
| ragkit-dev: CLI, FastAPI, Streamlit, npm generator | `cli.py`, `api.py`, `ui/app.py`, `generator/` (`rag-kit-dev`) |
| ragkit-dev: 290+ tests, offline CI with no API keys | 217 `def test_` in `tests/`, 75 `test(` in `generator/test/`; `.github/workflows/ci.yml` guard step fails if `GOOGLE_API_KEY` is set |
| ragkit-dev: personal project | 69 of 71 commits are yours (the other 2 are Dependabot) |
| FactoryBrain: cited Q&A through a Python RAG service | `Infrastructure/Services/AskService.cs` calls `PyRagClient` → `rag/main.py` (`/api/kb/{collection}/query`); `Citations` in `AskAnswerResponse.cs`. Corrected on 2026-10-30: the C# BM25 hybrid scorer (`HybridScorer.cs`) is no longer on the Ask path |
| FactoryBrain: risk tiers, approval queue | `Infrastructure/Services/AgentRunService.cs` (`approvalPending = risk != RiskTier.Low`) |
| FactoryBrain: vision-language defect detection, inspector review | `Infrastructure/Qc/LlmVisionDefectProvider.cs`, README "Quality inspection" |
| FactoryBrain: 174 xUnit, 57 Playwright tests, demo mode | `FactoryBrain.Api.Tests` (`[Fact]`/`[Theory]`), `frontend/e2e/tests/*.spec.ts`, README "Demo mode" |
| QueueStorm: English/Bangla/Banglish, JSON decision, fallback, safety filter | `Services/RuleBasedReasoningService.cs`, `ReasoningOrchestrator.cs` (8 s timeout), `SchemaValidator.cs`, `SafetyFilterService.cs` |
| Chokh: frame every ~2.5 s, Bengali prompt rules, deployed | README "How it works" and "Prompts", `Dockerfile`, Render URL in your profile README |
| NogorSathi: you built the demo interface | Your commits changed `Map-Copilot/FrontendTest/*` (scripted tool calls in `script.js`); Sayem Rahman wrote the README |
| rag-kit: gateway, FastAPI RAG service, per-KB Qdrant collections | `rag-kit/README.md`, `backend/Integrations/PythonRag/`, `rag/` |
| AI coursework from scratch | `AI-ML/Knn`, `K means cluster`, `A star search`, `CSP algo` (plain Python, no ML libraries) |
| ShilpoHubBD numbers | Carried over from the earlier verified CV report (`Webmotech_CV_Report.md`) |
| Achievements, ratings, hackathon count | Taken from your profile README. Not checkable from here; ratings change, so re-check before sending |

## Left out on purpose

- **Mango Fraud Detection.** The classifier returns a hard-coded prediction (`ai-service/models/mango_classifier.py`), so it can't be presented as a computer vision model yet.
- **The rest of the NogorSathi repository.** The large Python app added in the "final" commit is the VoiceAI-Asuna project. It isn't the NogorSathi agent, so the CV only claims the demo interface. The agent loop in that demo is scripted, so the CV says "demo interface", not a running agent.
- **Smart Shelf Robot and Nurture-Glow.** You made 1 of 43 and 4 of 48 commits.
- **The research proposals and statistics slides in this repository.** They were drafted by Claude, so they don't count as your own research briefs.
- **PyTorch and OpenCV as skills.** No project of yours runs a trained model yet, so they are listed under "Currently learning".
- **Phone number, CGPA and location.** They weren't in your earlier CVs or your profile.
