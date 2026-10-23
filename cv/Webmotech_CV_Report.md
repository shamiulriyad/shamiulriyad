# CV report: Software Engineer Internship, Webmotech

Apply to: careers@webmotech.com

## Files

| File | What it is |
|---|---|
| `Md_Shamiul_Islam_Riyad_Software_Engineer_Intern_CV.pdf` | Submission copy. One A4 page, selectable text, clickable links |
| `Md_Shamiul_Islam_Riyad_Software_Engineer_Intern_CV.html` | Editable source the PDF is built from (`node cv/build_software_engineer_cv.cjs`) |
| `Md_Shamiul_Islam_Riyad_Software_Engineer_Intern_CV.docx` | Editable Word copy, generated from the HTML (`python3 cv/build_docx.py`) |
| `original_backup/` | Untouched copy of the previous CV (HTML and PDF). The originals are also still in `cv/` |

Your request named `Md_Shamiul_Islam_Riyad_Backend_Engineer.pdf`. The file in the repo is `Md_Shamiul_Islam_Riyad_Backend_Engineer_Intern.pdf`. I used that one.

## 1. Main weaknesses in the previous CV

1. **Targeted at a backend CRM role.** The summary and skill order were written for a Credosis backend job. A general Software Engineer Internship screen looks for fundamentals (DSA, OOP), teamwork and breadth, and the old CV mentioned none of them.
2. **The testing claim had no evidence on the CV.** "xUnit with EF Core InMemory" is real, but it is only in `bruhcode-platform` (18 xUnit tests), which is not on the CV. None of the three listed projects uses xUnit. The real testing work in ShilpoHubBD (14 regression-check programs you wrote) was not mentioned.
3. **Your strongest evidence was missing:**
   - In ShilpoHubBD you wrote 790 of 964 backend commits and merged all 96 team pull requests. That is good proof of teamwork.
   - Reuse of a revoked refresh token revokes all of the user's sessions. This is a deliberate security choice, and the CV didn't mention it.
   - You also wrote 307 frontend commits in ShilpoHubBD. The old CV only said "used to connect my APIs to a UI".
4. **Competitive programming was undersold.** It was one line ("575+ problems") with no breakdown, contest count or ratings, and it sat under a generic heading. For an internship it is your clearest DSA signal.
5. **Avenzaq said "backend" and gave no ownership.** The repo has a React frontend, and every commit is yours. It now says "Personal project".
6. **Minor issues:**
   - The 2nd-runner-up award appeared only at the bottom, away from the project it was won with.
   - "4th place, UIU Team Contest" (from your profile README) was missing.
   - "C++" and "Java" had nothing in the CV backing them. C++ is now backed by the CP line.

## 2. Changelog

| Change | Why |
|---|---|
| Rewrote the summary for a general Software Engineer Internship: full-stack scope, CP problem solving, Git and pull-request teamwork | The announcement is general, so the CV now shows range, not only backend |
| Added a **Fundamentals** skills row (DSA, OOP with interfaces and DI, layered architecture) | Interns are screened on fundamentals. Each item is backed by the CP record or the ShilpoHubBD and Avenzaq code structure |
| Reordered languages (C# then C++); added transactions, Vite and regression checks; shortened wording | Puts first the skills the CV proves. Transactions come from Avenzaq checkout. Vite is in the ShilpoHubBD frontend |
| Changed the skills section from a two-column table to "Label: values" lines | In plain-text extraction the table separated labels from their values, which some ATS parsers read wrongly |
| ShilpoHubBD: added the commit share and 96 merged PRs, the reasoning behind the project split, BCrypt, token-reuse detection, 401 in the error mapping, and a testing bullet | Shows ownership, teamwork, engineering decisions and testing, all verified in the repo |
| Avenzaq: "backend" changed to "platform", "Personal project" added, bullets tightened | Matches the repo (React frontend, all commits yours) |
| E-Learning: added "23 EF Core migrations"; renamed "Platform API" to "Platform" | Migration count verified. The repo is full stack |
| Section renamed to "Competitive Programming and Achievements": per-judge counts, 55+ contests, LeetCode 1562 and CodeChef 1448 ratings, 4th place UIU Team Contest | Makes the DSA evidence specific. The Codeforces rating (1035) was left out because it is weaker than the other two |
| Removed the duplicate 2nd-runner-up mention from the project line | Saves space. It stays in Achievements |

No education details, dates, links or the name were changed.

## 3. Evidence for each claim

Verified on 2026-10-23 against fresh clones of the repos (default branch).

| Claim | Evidence |
|---|---|
| ShilpoHubBD: team of 5, 790 of 964 backend commits | `git shortlog -sn -- backend`: 790 shamiulriyad, 171 lamia233, 2 Riyad, 1 Emon. There are 5 human authors |
| ShilpoHubBD: merged 96 team PRs | `git log --merges --author=shamiulriyad`: 96 "Merge pull request" commits |
| 312 tables, 100+ migrations, 5 projects | `ShilpoHubDbContextModelSnapshot.cs` (312 `ToTable`), 101 migration files, `backend/src/ShilpoHubBD.{Domain,Application,Data,Infrastructure,Api}` |
| BCrypt, hashed rotating refresh tokens, reuse revokes all sessions | `Infrastructure/Security/BCryptPasswordHasher.cs`; `AuthService.RefreshTokenAsync` (`RevokeAllActiveForUserAsync` on reuse) |
| 9 roles, producer ownership checks | `Domain/Constants/RoleNames.cs`; `InventoryService` (`product.ProducerId != currentUserId`) |
| Inventory log, no negative stock, low-stock list | `InventoryService.cs` (`InventoryTransaction` with Previous/NewStock, `ConflictException`, `GetLowStockAsync`) |
| 400/401/404/409 mapping | `Api/Middlewares/GlobalExceptionHandler.cs` |
| 14 of 17 regression-check programs | `backend/tests/*`: you created 14 of the 17 directories. They are console programs that print PASS or fail, not an xUnit suite |
| FluentValidation, React, Vite, Axios | `Application.csproj`, `frontend/package.json`; you made 307 commits in `frontend/` |
| Avenzaq: transactional checkout, per-seller sub-orders, commission, rollback | `Backend/Services/OrderService.cs` (`BeginTransactionAsync`, `GroupBy(SellerId)`, throws before `CommitAsync`) |
| Avenzaq: roles, seller approval, own sub-orders only | `OrderService.cs` lines 211–242, `[Authorize(Roles=…)]` in controllers |
| Avenzaq: paged notifications, unread count, per-user SignalR groups | `Services/NotificationService.cs`, `Hubs/NotificationHub.cs` (`user-{id}` groups) |
| Avenzaq: personal project, .NET 10 | All 6 commits are yours; `Backend.csproj` targets `net10.0` |
| E-Learning: 48 tables, 23 migrations, 24 controllers, BCrypt | 48 `DbSet`s, 23 migration files (plus the model snapshot), 24 files in `Controllers/`, `Helpers/PasswordHasher.cs` |
| E-Learning: you built the backend | The other contributor (FaiyajJarif) changed only frontend files |
| E-Learning: competition scheduler, SignalR hubs | `Services/CompetitionLifecycleScheduler.cs` (`BackgroundService`), `MapHub` x2 in `Program.cs` |
| xUnit, EF Core InMemory | `bruhcode-platform/Backend.Tests` (xUnit 2.9.2, EF Core InMemory, 18 tests). That repo is not on the CV |
| C++ | `codeforces` repo: 330 `.cpp` solutions |
| Java | `java` repo (OOP and collections exercises); `lag-legend` (Java Swing game, per your profile README; not cloned) |

## 4. Claims I could not verify (please confirm)

| Claim | Status |
|---|---|
| 575+ solved (CF 252, CC 192, LC 131), 55+ contests, LC 1562, CC 1448 | The numbers match your profile README (`scripts/brand.py`) and add up correctly. I could not reach the judge sites from this environment. Check them before sending, because ratings change |
| 2nd runner-up, UIU CSE Project Show (Mar 2026); 4th place, UIU Team Contest (Jul 2026); 7 hackathons; top 70 of 700+ at Infinity AI BuildFest | Taken from your previous CV and profile README. There is no certificate in the repos to check them against |
| LinkedIn and portfolio links | The network policy blocked them here, so I couldn't test them. The three project repo links returned HTTP 200 |

## 5. Final checklist

- [x] One A4 page (PDF and DOCX both checked). Text is selectable and the fonts are embedded (Carlito, which has the same metrics as Calibri)
- [x] All 7 links are embedded in the PDF and DOCX (email, GitHub, LinkedIn, portfolio, 3 repos). The 3 repo links return HTTP 200
- [ ] LinkedIn, portfolio and the GitHub profile page could not be reached from this sandbox. Click each one once before sending
- [x] Plain-text extraction reads in order: one column, no tables, standard section headings
- [x] Formatting is consistent: same date style, project headers, italic stack lines, and the same verb tense in every bullet
- [x] Every technical claim has repo evidence (section 3). The xUnit evidence is in a repo that isn't listed (section 6)
- [x] No professional experience claimed. All work is described as team, personal or academic
- [x] Name, university, dates and links are unchanged. Expected graduation stays 2027
- [x] Original CV kept (`cv/original_backup/` and the original files in `cv/`)
- [x] Nothing committed, pushed or published

## 6. Recommendations before you apply

1. **Fix BRUHCODE password hashing.** If you keep "xUnit" on the CV, an interviewer may open `bruhcode-platform` because that is where the tests are. It hashes passwords with unsalted SHA-256 (`AuthController.cs:59`, `UserController.cs:319,325`). Moving to BCrypt, as ShilpoHubBD already does, is a small change. Another option is to remove "xUnit, EF Core InMemory" from the CV.
2. **Missing information you could add** (I did not guess any of it): CGPA, a phone number, and relevant coursework (for example Data Structures, Algorithms, DBMS, OOP). Bangladeshi internship screens often expect a CGPA and a phone number.
3. **Python was left out on purpose**, because your earlier instructions removed it. For a general SWE internship, your `AI-ML` repo (A* search, constraint satisfaction from scratch) would support adding it to Languages if you want.
4. Send the PDF, not the DOCX.

## Update: skills section replaced with your wording

You replaced the Technical Skills section with your own wording (Languages, Backend, Databases, Engineering, Frontend). Every item has evidence in the table above. Some skills are no longer listed: Java, JavaScript as a language, xUnit, SignalR, FluentValidation and the testing tools. The xUnit and BRUHCODE password-hashing point in section 6 no longer applies to this CV.
