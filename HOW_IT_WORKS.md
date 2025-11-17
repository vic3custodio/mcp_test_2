# How It Works: Keyword-Based Search Flow

## Traditional Approach ❌

```
User Email → Copilot → "Need file at configs/reports/daily_settlement.sql"
                         ↓
                    You remember exact path?
                         ↓
                    Manual search through folders
                         ↓
                    Find file (maybe)
```

## Our Approach ✅

```
User Email → Copilot → search_sql_configs("settlement report")
                         ↓
                    Metadata Index (instant lookup)
                         ↓
                    All files with "settlement" + "report" keywords
                         ↓
                    - daily_settlement_report.sql
                    - settlement_exceptions.sql
                    - settlement_reconciliation.sql
```

## The System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     VS Code Copilot                         │
│  (User pastes email and asks for help)                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Trade Surveillance MCP Server                  │
│                                                             │
│  Tool 1: parse_email_inquiry                               │
│    └─> Extract: trade IDs, dates, issue type              │
│                                                             │
│  Tool 2: search_sql_configs (keyword search)               │
│    └─> Query: "settlement failed"                          │
│         └─> Metadata Index → Finds matching SQL files      │
│                                                             │
│  Tool 3: search_java_code (keyword search)                 │
│    └─> Query: "report generator"                           │
│         └─> Metadata Index → Finds matching Java classes   │
│                                                             │
│  Tool 4: execute_java_report                               │
│    └─> Run: java -cp ... ReportGenerator config.sql       │
│                                                             │
│  Tool 5: rebuild_metadata_index                            │
│    └─> Scan and index all annotated files                 │
│                                                             │
│  Tool 6: generate_response_summary                         │
│    └─> Create formatted summary for user                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Metadata Index (JSON)                      │
│                                                             │
│  {                                                          │
│    "sql_configs": {                                         │
│      "daily_settlement.sql": {                             │
│        "keywords": ["settlement", "daily", "trade"],       │
│        "type": "compliance_report",                        │
│        "description": "Daily settlement report"            │
│      }                                                      │
│    },                                                       │
│    "java_classes": {                                        │
│      "ReportGenerator.java": {                             │
│        "keywords": ["report", "generator", "settlement"],  │
│        "type": "report_generator",                         │
│        "methods": ["generateReport", "executeQuery"]       │
│      }                                                      │
│    }                                                        │
│  }                                                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│            Your Files (with annotations)                    │
│                                                             │
│  SQL Configs:                                              │
│  ┌──────────────────────────────────────────────────┐     │
│  │ -- @keywords: settlement, daily, reconciliation   │     │
│  │ -- @type: compliance_report                      │     │
│  │ -- @description: Daily settlement report          │     │
│  │ SELECT * FROM trades WHERE ...                    │     │
│  └──────────────────────────────────────────────────┘     │
│                                                             │
│  Java Classes:                                             │
│  ┌──────────────────────────────────────────────────┐     │
│  │ /**                                               │     │
│  │  * @keywords report, generator, settlement        │     │
│  │  * @type report_generator                         │     │
│  │  * @description Generates settlement reports      │     │
│  │  */                                               │     │
│  │ public class ReportGenerator { ... }              │     │
│  └──────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Example Conversation Flow

```
Step 1: User Email
┌──────────────────────────────────────────────────┐
│ From: trader@company.com                         │
│ Subject: Failed Settlement T12345                │
│                                                  │
│ Hi, trade T12345 failed to settle yesterday.    │
│ Need the settlement report and audit trail.     │
└──────────────────────────────────────────────────┘
                    ↓
Step 2: User Action
┌──────────────────────────────────────────────────┐
│ User: [Pastes email in Copilot]                 │
│                                                  │
│ "Can you help investigate this?"                │
└──────────────────────────────────────────────────┘
                    ↓
Step 3: Copilot Processing
┌──────────────────────────────────────────────────┐
│ Copilot:                                         │
│ 1. parse_email_inquiry(email)                   │
│    → trade_id: T12345, issue: failed_settlement │
│                                                  │
│ 2. search_sql_configs("settlement failed")      │
│    → Found: daily_settlement_report.sql         │
│    → Found: settlement_exceptions.sql           │
│                                                  │
│ 3. search_java_code("settlement report")        │
│    → Found: SettlementReportGenerator.java      │
│                                                  │
│ 4. execute_java_report(...)                     │
│    → Generated: /reports/settlement_T12345.csv  │
└──────────────────────────────────────────────────┘
                    ↓
Step 4: Result
┌──────────────────────────────────────────────────┐
│ Copilot: I've investigated trade T12345:        │
│                                                  │
│ Used configs:                                    │
│ - daily_settlement_report.sql                   │
│ - settlement_exceptions.sql                     │
│                                                  │
│ Generated report:                                │
│ - /reports/settlement_T12345.csv                │
│                                                  │
│ The report shows the settlement failed due to    │
│ insufficient funds. Recommend following up with  │
│ the counterparty.                                │
└──────────────────────────────────────────────────┘
```

## Key Benefits

### 1. No Memory Required
- ❌ Before: "Where did I put that settlement SQL?"
- ✅ After: "Search for 'settlement'"

### 2. Semantic Understanding
- ❌ Before: Must know exact file names
- ✅ After: Search by what files do

### 3. Refactoring-Friendly
- ❌ Before: Move file → breaks everything
- ✅ After: Move file → keywords still work

### 4. AI-Optimized
- ❌ Before: "Get file at path X"
- ✅ After: "Find files about settlement reports"

## Implementation Details

### Annotation Extraction

**SQL Files:**
```python
# Regex pattern: -- @keywords: (.+)
# Extracts: ["trade", "settlement", "daily"]
```

**Java Files:**
```python
# Regex pattern: * @keywords (.+)
# Extracts: ["report", "generator", "settlement"]
```

### Search Algorithm

```python
1. Parse query: "settlement report" → ["settlement", "report"]
2. For each indexed file:
   - Combine: keywords + type + description
   - Check if any query term matches
3. Return all matches with metadata
```

### Index Storage

```json
{
  "file_name.sql": {
    "keywords": [...],
    "type": "...",
    "description": "...",
    "file_path": "full/path/to/file"
  }
}
```

---

**Ready to try it? See [QUICKSTART.md](QUICKSTART.md) to annotate your first file!**
