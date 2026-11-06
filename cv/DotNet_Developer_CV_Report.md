# CV report: Junior .NET Developer

## Files

| File | What it is |
|---|---|
| `Md_Shamiul_Islam_Riyad_DotNet_Developer_CV.pdf` | Submission copy. One A4 page, single column, selectable text, embedded fonts, clickable links |
| `Md_Shamiul_Islam_Riyad_DotNet_Developer_CV.docx` | Editable Word copy (`python3 cv/build_docx.py Md_Shamiul_Islam_Riyad_DotNet_Developer_CV`) |
| `Md_Shamiul_Islam_Riyad_DotNet_Developer_CV.html` | Source for the PDF (`node cv/build_dotnet_developer_cv.cjs`) |

The starting point was the Software Engineer Intern CV, the newest .NET-focused CV in this folder, including your own wording for the skills section. That file is unchanged.

## How the CV maps to the job

| The job asks for | Where the CV shows it |
|---|---|
| C# and .NET | Tagline, summary, skills (.NET 8 and .NET 10), and the stack line of every project |
| ASP.NET / ASP.NET Core | Three ASP.NET Core Web API projects |
| REST API development | 24 REST controllers (E-Learning), role-secured endpoints (Avenzaq), status-code mapping (ShilpoHubBD) |
| REST API integration | **New:** 15 typed HttpClient clients for third-party REST APIs in ShilpoHubBD; React and Axios clients for your own APIs |
| Database design and integration | 312-table and 48-table PostgreSQL schemas, EF Core migrations, transactional checkout |
| Clean, scalable, maintainable code | Split into Domain, Application, Data, Infrastructure and Api projects; dependency injection; interfaces in front of external APIs |
| Debugging and troubleshooting | Global exception handler, API testing with Swagger and .http files, regression-check programs, error handling on external calls |
| Team collaboration and best practices | Team of 5, 96 merged pull requests, Git and GitHub workflow |

## What changed from the Software Engineer Intern CV

| Change | Why |
|---|---|
| Added a tagline: "Junior .NET Developer · C# · ASP.NET Core · REST APIs · PostgreSQL" | The recruiter sees the target role and the main keywords first |
| Rewrote the summary for a junior .NET role, renamed to "Professional Summary" | Puts C#, ASP.NET Core, EF Core, PostgreSQL and REST APIs first, and it says "junior" outright |
| Skills: new ".NET and Backend", "Security" and "Practices and Tools" lines | Matches the job's wording. FluentValidation, SignalR, background services, transactions, Swagger and .http files are all backed by the repos (see below) |
| Kept your honest frontend line, marked "supporting" | The role is backend. Your own note that JavaScript is still developing stays |
| ShilpoHubBD: new bullet on REST API integration | This is your strongest evidence for "REST API integration" and the old CV left it out |
| ShilpoHubBD: merged-PRs line moved into a teamwork and testing bullet | Matches "team collaboration" |
| E-Learning: added testing with Swagger and .http files | Covers "debugging and troubleshooting" with real practice |
| "Competitive Programming and Achievements" became "Problem Solving and Achievements", shortened | Still shows problem solving, but takes less space on a .NET CV |

No name, contact details, education, dates or links were changed.

## Evidence for new claims

Checked on 2026-11-06 against fresh clones of the default branches.

| Claim | Evidence |
|---|---|
| 15 typed HttpClient clients for third-party REST APIs | `ShilpoHubBD.Infrastructure/DependencyInjection.cs` (15 `AddHttpClient<IInterface, Impl>` calls): Gemini, `OsrmRoutingProvider`, `NominatimGeocodingProvider`, `OverpassPoiClient` |
| Written by you | `git log` on every HttpClient provider file and `DependencyInjection.cs`: only shamiulriyad |
| Timeouts, failed responses, network errors | `client.Timeout` from `GeminiOptions`; `IsSuccessStatusCode` checks and `catch (HttpRequestException or TaskCanceledException)` in `OsrmRoutingProvider.cs` and `NominatimGeocodingProvider.cs` |
| Rule-based fallbacks | `GeminiReviewModerationProvider` falls back to `RuleBasedReviewModerationProvider` ("so review creation is never affected"); the same pattern applies to repeated complaints and producer impact |
| Swagger | `AddSwaggerGen`/`UseSwagger` in `Program.cs` of all three projects |
| .http request files | `Avenzaq/Backend/Backend.http`; `DatabaseHub/E-Learning/backend/backend.http` and `universities.http` |
| .NET 8 and .NET 10 | `TargetFramework` `net8.0` (ShilpoHubBD, E-Learning) and `net10.0` (Avenzaq) |
| Axios | `package.json` of all three frontends |

All other claims are the same as in the Software Engineer Intern CV, and their evidence is in `Webmotech_CV_Report.md`, section 3.

## Left out on purpose

- **".NET Framework".** Your projects use modern .NET (8 and 10), not the older .NET Framework 4.x. The CV says ".NET", which ATS keyword matching still picks up. If an interviewer asks, you can say you have used modern .NET only.
- **Python, AI/ML, RAG work.** Not relevant to this role. The Gemini integration is shown only as an example of REST API integration.
- **The ShilpoHubBD Python services.** The .NET side calls them over HTTP, but naming them would add a non-.NET language.
- **xUnit.** It appears only in `bruhcode-platform`, which still hashes passwords with unsalted SHA-256. Don't list it until that is fixed.
- **SOLID, Docker, CI/CD, unit testing, Azure, microservices.** No evidence in these three repos, so not claimed.
- **Codeforces rating, contest count.** Removed to save space.

## Please confirm before sending

| Item | Status |
|---|---|
| 575+ problems, ratings, contest placings, hackathons | Copied from your previous CV and profile README. I can't reach the judge sites from here, and ratings change |
| LinkedIn and portfolio links | Not reachable from this environment. Click each one once |
| Missing details you could add | CGPA, phone number, relevant coursework (for example OOP, Data Structures, Database Management Systems, Software Engineering). I didn't guess any of them |

## Checklist

- [x] One A4 page in both PDF and DOCX (DOCX checked by converting it to PDF)
- [x] Single column, standard section headings, no tables. Plain-text extraction reads in order
- [x] No employment history claimed. Every project is marked personal, team or academic
- [x] Every technical claim has evidence in a repo
- [x] Previous CVs left unchanged
