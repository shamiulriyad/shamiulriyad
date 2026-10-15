# CV: Backend Engineer Intern (CRM), Credosis

- **PDF:** [`Md_Shamiul_Islam_Riyad_Backend_Engineer_Intern.pdf`](Md_Shamiul_Islam_Riyad_Backend_Engineer_Intern.pdf) (one A4 page, selectable text, clickable links)
- **Source:** [`Md_Shamiul_Islam_Riyad_Backend_Engineer_Intern.html`](Md_Shamiul_Islam_Riyad_Backend_Engineer_Intern.html)
- **Rebuild:** `node cv/build.cjs` (needs `playwright` and Chromium)

## Where each claim comes from

Every bullet was checked against the repository source. The tests were not run here because the .NET SDK was unavailable.

| Claim | Evidence |
|---|---|
| rag-kit: Owner/Admin/Member roles, 404 for non-members | `backend/Models/Enums.cs` (`MemberRole`), `backend/Authorization/ResourceAuthorizationService.cs` |
| rag-kit: refresh-token rotation, reuse ends all sessions | `backend.Tests` (`RefreshRotatesAndReusingTheOldTokenIsRejected`, `ReplayingARevokedTokenLaterEndsEverySession`) |
| rag-kit: single-use reset/verify tokens stored as hashes | `backend.Tests` (`OnlyTheTokenHashIsStored`, `ResetFlowChangesPasswordAndTokenIsSingleUse`) |
| rag-kit: plan limits, support tickets, activity logs | `Services/PlanLimitService.cs`, `SupportService.cs`, `ActivityLogService.cs` |
| rag-kit: 40 xUnit tests | `[Fact]`/`[Theory]` count in `backend.Tests/*.cs` (xUnit + EF Core InMemory) |
| Avenzaq: transactional checkout, per-seller sub-orders, commission, stock rollback | `Backend/Services/OrderService.cs` `CheckoutAsync` |
| Avenzaq: role checks, seller approval, own sub-orders only | `[Authorize(Roles=...)]` in `Controllers/`, `OrderService.UpdateSellerOrderStatusAsync` |
| Avenzaq: paged notifications, unread count, per-user SignalR group | `Services/NotificationService.cs`, `Hubs/NotificationHub.cs` |
| E-Learning: 48 tables, keys/indexes/delete rules, migrations | `ApplicationDbContext` (48 `DbSet`s), `Migrations/` |
| E-Learning: 24 controllers, Student/Teacher/Admin roles, BCrypt | `Controllers/`, `Helpers/PasswordHasher.cs` |
| E-Learning: competition scheduler, SignalR | `Services/CompetitionLifecycleScheduler.cs`, `MapHub` in `Program.cs` |

Left out on purpose:
- **ShilpoHubBD.** It is a five-person team project with about 133k lines of C# and 170 controllers, so it is hard to defend in an interview as your own work.
- **E-Learning error handling.** Its `ExceptionMiddleware` returns `exception.Message` with a 500 for every error, so error handling is not claimed for that project.
- **The "17 regression suites" from the old CV.** They are console PASS/FAIL programs, not a test framework.
