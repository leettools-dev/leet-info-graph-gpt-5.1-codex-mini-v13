## Product Requirements Document (PRD)

**Product name (working):** Research Infographic Studio

---

### 1) Summary

Build a full-stack web application where users sign in with Google, submit research prompts, and receive:

1. an **AI-generated infographic** (visual summary),
2. an **explanatory article** (structured narrative),
3. **supporting sources** (citations with links/metadata).

Users can browse a searchable **research history**, revisit any result, and **export** (PNG/PDF for infographic, Markdown/PDF for article, JSON/CSV for citations).

---

### 2) Goals and Success Metrics

#### Goals

* Reduce the time to go from “question” → “shareable, cited infographic + article”.
* Provide trustworthy, traceable outputs (citations, confidence, provenance).
* Make outputs easy to revisit, refine, and export.

#### Success Metrics (initial targets)

* **Activation:** ≥ 40% of signed-in users generate at least 1 research result.
* **Time-to-first-result:** median ≤ 90 seconds for a standard prompt.
* **Export rate:** ≥ 20% of completed results exported at least once.
* **Return usage:** ≥ 25% of weekly active users open history and revisit prior work.
* **Citation coverage:** ≥ 90% of “factual claims” sections contain citations.
* **User satisfaction:** CSAT ≥ 4.2/5 on “useful & trustworthy”.

---

### 3) Non-Goals (Out of Scope for MVP)

* Team collaboration, shared workspaces, or real-time co-editing.
* Custom infographic design editor (full Figma-like tooling).
* Deep domain compliance workflows (medical/legal certification).
* Offline mobile app (responsive web only for MVP).

---

### 4) Target Users & Personas

1. **Students / Learners**: need fast understanding with sources for papers.
2. **Content creators / Marketers**: need shareable visuals + narrative.
3. **Analysts / Researchers**: need traceability, citations, exportable artifacts.
4. **Educators**: need classroom-ready summaries with sources and visuals.

---

### 5) Core User Journeys

#### Journey A: Sign in and create a research result

1. User clicks **Sign in with Google**.
2. User enters a **research prompt** (optional constraints: tone, audience, region, date range).
3. System retrieves sources, generates outline, writes article, produces infographic.
4. User sees results page with **Infographic + Article + Sources** and can export.

#### Journey B: Browse history and export

1. User opens **History**.
2. Filters/searches by keyword/tag/date.
3. Opens a past result.
4. Exports infographic/article/sources in chosen formats.

#### Journey C: Iterate / refine

1. User clicks **Refine**.
2. Adds instructions (“focus on 2022–2025”, “simplify for 8th grade”, “add charts”).
3. System generates a new version linked to the original.

---

### 6) Functional Requirements

#### 6.1 Authentication & Accounts

* **Google OAuth** sign-in.
* Store: user id, email, name, avatar, created_at, last_login.
* Optional: allow user to delete account + data export (privacy).

**Acceptance criteria**

* User can sign in/out reliably.
* Refresh tokens handled securely (httpOnly cookies or secure token storage).

---

#### 6.2 Prompt Submission

* Prompt editor with:

  * Main prompt text
  * Optional settings: audience, tone, length, preferred citation style (APA/MLA/links), time range, region/language
  * “Include counterpoints” toggle (optional)
* Prompt validation: length limits, unsafe content checks.

**Acceptance criteria**

* Prompt creation returns a job id and starts processing.
* UI shows progress states.

---

#### 6.3 Research Pipeline (Sources + Synthesis)

**MVP approach**

* Source acquisition via one of:

  * Web search API + page fetching
  * Curated sources list (e.g., Wikipedia + major publishers) as a fallback
* Steps:

  1. Query expansion + search
  2. Fetch top sources
  3. Extract key claims + metadata
  4. Generate outline
  5. Write article with citations
  6. Generate infographic spec
  7. Render infographic image(s)

**Source metadata**

* Title, publisher, URL, publish date (if available), accessed date, snippet/summary, reliability signals (optional)

**Acceptance criteria**

* Every result includes ≥ N sources (configurable; e.g., 5) unless user requests otherwise.
* Article contains citations mapped to sources (clickable).
* System shows “Last updated / accessed on” for sources.

---

#### 6.4 Output: Explanatory Article

* Structured sections (default):

  * Overview
  * Key points (bullets)
  * Detailed explanation
  * Implications / applications
  * Limitations / uncertainties
  * Sources
* Inline citations (e.g., [1], [2]) that link to the sources list.
* “Confidence / uncertainty notes” section (model-generated, non-fabricated tone).

**Acceptance criteria**

* Article renders correctly with citations.
* No broken citation references (every citation index exists in sources list).

---

#### 6.5 Output: Infographic Generation

**Infographic types (MVP)**

* Timeline
* Comparison table
* Process/flow diagram
* Key statistics callouts
* “Top 5 takeaways” visual

**Implementation**

* Generate an **Infographic Spec** (JSON) describing layout blocks, text, icons, charts, and data.
* Render via:

  * Server-side SVG → PNG, or
  * Canvas renderer in headless browser

**Acceptance criteria**

* Infographic renders as PNG (and optionally SVG/PDF).
* Visual includes a title, date, and citation marker(s) when relevant (e.g., small [1][3]).

---

#### 6.6 History & Versioning

* History list: title (auto), prompt snippet, created date, tags, status, versions count.
* Detail view shows:

  * Prompt
  * Outputs
  * Version tree / “Regenerate” / “Refine”
* Search and filters: keyword, date range, tags.

**Acceptance criteria**

* User can retrieve all past results (paginated).
* Versions are linked (parent_result_id).

---

#### 6.7 Export & Sharing

**Export formats**

* Infographic: PNG, PDF (optional SVG)
* Article: PDF, Markdown, HTML
* Sources: BibTeX, JSON, CSV (MVP can start with JSON + CSV)

**Share**

* Private by default.
* Optional share link (V2): public read-only page with redaction controls.

**Acceptance criteria**

* Export includes correct version, timestamps, and sources list.
* Downloads work across modern browsers.

---

#### 6.8 Notifications (Optional for MVP)

* In-app status updates (queued → running → completed → failed).
* Email notifications (V2).

---

### 7) Admin & Operations Requirements

* Admin dashboard (MVP-light):

  * Job status monitoring
  * Error logs
  * Abuse reports
  * Usage metrics (requests per user/day)

---

### 8) Data Model (Conceptual)

* **User**
* **ResearchRequest**: user_id, prompt, settings, status, created_at
* **ResearchResult**: request_id, version, title, article_md/html, infographic_assets, created_at
* **Source**: result_id, url, title, publisher, publish_date, accessed_at, excerpt, reliability_notes
* **Asset**: result_id, type (png/pdf/svg), storage_key, size, created_at

---

### 9) System Architecture (High Level)

* **Frontend**: Next.js/React (or similar), responsive UI
* **Backend API**: Node/Express or Python/FastAPI
* **Auth**: Google OAuth
* **Job Queue**: for long-running generation (e.g., Redis + worker)
* **Storage**: Postgres for metadata; object storage (S3-compatible) for assets
* **AI Services**:

  * LLM for outline/article/spec
  * Image rendering service for infographic

---

### 10) Safety, Trust, and Compliance

* **No hallucinated sources**: citations must map to fetched sources.
* Mark uncertainty; avoid definitive claims when sources are weak.
* Content moderation for prompts and outputs (hate, self-harm, illegal instructions, etc.).
* Respect Google OAuth policy requirements and user data handling.
* Clear UI labels: “AI-generated”, “Sources last accessed on…”.

---

### 11) Performance & Reliability

* Typical job completion target: 30–120 seconds depending on prompt complexity.
* Retry strategy for fetch failures.
* Cache fetched pages (time-limited) to reduce cost.
* Rate limiting per user; abuse prevention.

---

### 12) UX Requirements (MVP Screens)

1. Landing + Google sign-in
2. New Research: prompt editor + settings
3. Job Progress: stepper (search → extract → write → render)
4. Result Detail: infographic + article + sources + export buttons
5. History: list + filters + search
6. Account: delete/export data, usage summary

---

### 13) MVP Scope vs V2

#### MVP (must have)

* Google sign-in
* Prompt submission
* Source retrieval + citations
* Article generation
* Infographic generation (2–3 templates)
* History list + detail
* Export PNG + Markdown/HTML + JSON/CSV sources

#### V2 (nice to have)

* Shareable links with access control
* More infographic templates + style themes
* Collaboration / folders / tags automation
* Email notifications
* User feedback loop (“This claim is wrong” → regenerate with constraints)
* Plagiarism/citation style formatting (APA/MLA) polish

---

### 14) Open Questions

* Which web search / source acquisition method is approved (API choice, cost, licensing)?
* Citation style requirements (link list vs strict APA/MLA)?
* Do we support multiple languages in MVP?
* Storage retention policy (default delete after X months vs indefinite)?
* Export fidelity requirements (print-ready PDF, vector SVG, etc.)?

---

### 15) Acceptance Criteria (Release Gate)

* A user can sign in with Google, submit a prompt, and receive:

  * a rendered infographic (PNG),
  * an article with consistent citations,
  * a sources list with URLs and metadata.
* User can view history and open any past result.
* User can export infographic and article successfully.
* No outputs include fabricated citations (citations must match stored sources).
