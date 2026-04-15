# snowflake-adventureworks-migration

> Enterprise database migration framework that uses GPT-4 to convert T-SQL views and stored procedures to Snowflake, the part every migration tool fails at.

![Python](https://img.shields.io/badge/Python-3670A0?style=flat-square&logo=python&logoColor=ffdd54)
![Snowflake](https://img.shields.io/badge/Snowflake-%2300AEFF.svg?style=flat-square&logo=snowflake&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI%20GPT--4-412991?style=flat-square&logo=openai&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-%230db7ed.svg?style=flat-square&logo=docker&logoColor=white)
![Parquet](https://img.shields.io/badge/Apache%20Parquet-50ABF1?style=flat-square)

---

## The problem with database migrations

Moving tables is the easy part. Every migration tool handles `SELECT * FROM table`. What they don't handle, and what breaks every enterprise migration, is the **business logic layer**: views with XML parsing, stored procedures with cursors and recursive CTEs, T-SQL-specific types that have no Snowflake equivalent, and SQL Server syntax that silently produces wrong results instead of errors.

This is where migrations stall for weeks. This project solves it with a rule-based engine for the predictable parts and **GPT-4 for everything else.**

---

## How the AI layer works

T-SQL and Snowflake Scripting are fundamentally different languages. Parameter syntax, transaction handling, error blocks, type systems, all diverge. Static rules cover the predictable conversions. GPT-4 handles the rest.

**Every view and procedure goes through a 2-tier pipeline:**

```
T-SQL View / Procedure
        │
        ▼
Static rule engine (fast, free, deterministic)
brackets → removed | schemas → UPPERCASE
ISNULL → IFNULL | GETDATE() → CURRENT_TIMESTAMP()
        │
   Deploys? ──YES──► Snowflake ✓
        │
        NO
        ▼
Complexity detection
hierarchyid / CURSOR / MAXRECURSION / >1500 chars?
        │
   ┌────┴────┐
Simple     Complex
prompt     prompt
        │
        ▼
GPT-4 conversion (temperature=0.1 for determinism)
        │
        ▼
Post-AI cleanup layer
strip markdown · fix schema quoting · remove SQL comments
re-apply static type rules · fix duplicate schema patterns
        │
        ▼
Deploy to Snowflake ──► Verify
```

**GPT output is never trusted directly.** LLMs make the same class of mistakes consistently, quoting schema names incorrectly, leaving SQL comments that break Snowflake's parser, adding conversational preambles before the SQL. A deterministic cleanup layer catches all of these before deployment. Cheaper and faster than asking the model to self-correct.

**Complexity is detected before the API call.** Procedures containing `hierarchyid`, `CURSOR`, `OPTION (MAXRECURSION)`, or over 1,500 characters get a more detailed prompt automatically. Two prompt templates, one decision, meaningful accuracy improvement.

**Prompts are versioned config, not hardcoded strings.** All LLM instructions live in `config/llm_prompts.json` — separate from application logic. Improving a prompt is a one-line edit, not a code deployment.

---

## Results

| Metric | Result |
|---|---|
| Tables migrated | 71 / 71 — 100% |
| Rows transferred | 760,837 across 6 schemas |
| Migration time | ~3 minutes |
| Manual intervention | Zero |
| Throughput | ~6,500 rows/second |

| Schema | Tables | Rows |
|---|---|---|
| Production | 25 | 350K |
| Sales | 19 | 253K |
| Person | 13 | 141K |
| Purchasing | 5 | 13K |
| HumanResources | 6 | 934 |
| DBO | 3 | 1.6K |

---

## Edge cases that break most pipelines

SQL Server has ~40 data types. Snowflake has ~15. These are the gaps that silently corrupt data in automated migrations:

**`hierarchyid`** — SQL Server's tree-structure type has no Snowflake equivalent. Cast to `VARCHAR(4000)` during extraction, preserving the hierarchy string for post-migration transformation.

**`geography`** — Parquet treats geography as a complex object and fails silently. Handled via a dedicated CSV pipeline converting spatial data to WKT (Well-Known Text) before load.

**`IDENTITY` columns** — No `IDENTITY` in Snowflake. Auto-converted to sequences with `DEFAULT seq.NEXTVAL` — referential integrity preserved.

**`NULL` propagation** — Pandas silently converts `None` to the string `"None"` in certain cases. Explicit cleanup before every Parquet write prevents downstream corruption.

**`NVARCHAR` sizing** — SQL Server uses 2 bytes per character. `NVARCHAR(100)` becomes `VARCHAR(50)`. The type mapper handles this using source length metadata — no manual intervention.

---

## Testing & Validation

**Procedure tests run against the actual Snowflake database — not mocks.** The `uspUpdateEmployeeHireInfo` test captures before/after state on a live employee record, executes the procedure with a timestamped unique job title, and asserts both `JobTitle` and `HireDate` updated correctly.

**Row count assertions fire after every table migration.** Silent mismatches — the most common failure mode in bulk migrations — are caught at the table level, not discovered later when a dashboard shows wrong numbers.

---

## Engineering Decisions

**JSON-driven type mapping, not hardcoded logic.** All 30+ conversion rules live in `config/type_mapping.json`. Adding a new type is a one-line config edit — no code changes, no regression risk.

**Discovery before conversion.** Schema introspection runs once and outputs `discovery_report.json`. Every downstream script reads from this artifact. **The SQL Server connection is only needed once** — the rest of the pipeline runs offline.

**Transport via Parquet, not CSV.** Columnar format gives 3–5x speed improvement, preserves type fidelity, and integrates cleanly with Snowflake's parallel `COPY INTO` bulk loader.

**Separation of concerns enforced by script numbering.** Each script does exactly one thing. Running them out of order fails explicitly. Discovery → Convert → Test → Execute → Migrate → Validate.

---

## Quick Start

```bash
# 1. Start SQL Server and restore AdventureWorks
docker-compose up -d
./setup/install_adventureworks.sh

# 2. Python environment
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. Add credentials (Snowflake + OpenAI)
cp .env.example .env

# 4. Run the full pipeline
cd scripts
python 01_discover_schema.py          # Schema introspection → discovery_report.json
python 02_convert_schema.py           # DDL generation → snowflake_ddl/*.sql
python 03_test_snowflake.py           # Connection verification
python 04_execute_ddl.py              # Create schemas, tables, sequences
python 05_migrate_data.py             # Bulk migration via Parquet — ~3 min
python 06_load_person_address_csv.py  # Spatial data handler
python 07_migrate_views_ai.py         # Views — rules + GPT-4 fallback
python 08_migrate_procedures_ai.py    # Procedures — rules + GPT-4 + complexity routing
python 09_test_procedures.py          # Live validation suite
```

---

## Project Structure

```
├── config/
│   ├── type_mapping.json           # 30+ SQL Server → Snowflake type conversion rules
│   └── llm_prompts.json            # GPT-4 prompts (views, XML views, simple/complex procedures)
├── scripts/
│   ├── 01_discover_schema.py       # Introspects SQL Server system catalogs
│   ├── 02_convert_schema.py        # Generates Snowflake-compatible DDL
│   ├── 05_migrate_data.py          # Extract → Parquet → COPY INTO + validation
│   ├── 07_migrate_views_ai.py      # 2-tier view migration with GPT-4 fallback
│   ├── 08_migrate_procedures_ai.py # Procedure migration with complexity routing
│   └── 09_test_procedures.py       # Live validation against migrated Snowflake DB
└── snowflake_ddl/                  # Generated SQL artifacts (schemas, tables, PKs, FKs)
```

---

## Topics
`snowflake` `data-engineering` `llm` `gpt-4` `database-migration` `sql-server` `etl` `parquet` `python` `openai` `data-warehouse` `ai-assisted-migration`
