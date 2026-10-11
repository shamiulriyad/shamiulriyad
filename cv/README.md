# CV: Backend Engineer Intern (CRM), Credosis

- **PDF:** [`Md_Shamiul_Islam_Riyad_Backend_Engineer_Intern_Credosis.pdf`](Md_Shamiul_Islam_Riyad_Backend_Engineer_Intern_Credosis.pdf) (one A4 page, selectable TrueType text, clickable links)
- **Source:** [`Md_Shamiul_Islam_Riyad_Backend_Engineer_Intern_Credosis.html`](Md_Shamiul_Islam_Riyad_Backend_Engineer_Intern_Credosis.html)
- **Rebuild:** `node cv/build.cjs` (needs `playwright` and Chromium)

## Where each claim comes from

Every project bullet was checked against the repository source, not only the README.

| Claim | Evidence |
|---|---|
| ShilpoHubBD: five-project Clean Architecture | `backend/src/ShilpoHubBD.{Domain,Application,Data,Infrastructure,Api}` |
| ShilpoHubBD: hashed refresh tokens, rotated and revoked | `Application/Services/Auth/AuthService.cs` (`ReplacedByTokenHash`, `RevokedAt`) |
| ShilpoHubBD: nine roles, ownership checks | `Domain/Constants/RoleNames`, `ProducerOrderService.cs` |
| ShilpoHubBD: rate limiting, global exception handler | `Api/Program.cs` (`AddRateLimiter`), `Api/Middlewares/GlobalExceptionHandler.cs` |
| ShilpoHubBD: ranked full-text search | `Data/Search/PostgresProductSearchProvider.cs` (`PlainToTsQuery`, `Rank`) |
| ShilpoHubBD: payment callback, third-party APIs | `PaymentsController` `/{id}/callback`; Nominatim/OSRM/Gemini options in Infrastructure |
| ShilpoHubBD: 17 regression suites | `backend/tests/*Regression` (console harnesses with fake repositories) |
| Avenzaq: transactional per-seller checkout | `Backend/Services/OrderService.cs` (`BeginTransactionAsync`, `GroupBy(SellerId)`, stock checks) |
| Avenzaq: seller approval, ownership on status updates | `AdminService.ApproveSellerAsync`, `OrderService.UpdateSellerOrderStatusAsync` |
| Avenzaq: notifications plus SignalR hub | `NotificationService.cs`, `Hubs/NotificationHub.cs`, `frontend/src/hooks/useNotificationHub.js` |
| E-Learning: 48 tables, 25 controllers | `ApplicationDbContext.cs` (48 `DbSet`s), `Controllers/` |
| E-Learning: background service, SignalR pushes | `CompetitionLifecycleScheduler.cs`, `IHubContext` in `EnrollmentService`/`CommunityService` |

Deliberately left out because the code does not support them: payment processing in the E-Learning API (its payment and webhook methods return "Not implemented"), and a seller-must-be-approved-to-list rule in Avenzaq (most of those checks are commented out).
