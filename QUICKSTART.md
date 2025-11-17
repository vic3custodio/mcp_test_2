# Quick Start: Keyword-Based File Search

Stop searching by file paths! Use metadata keywords instead.

## ⚡ 3-Step Setup

### 1. Annotate Your Files (5 minutes)

**SQL Files** - Add at the top:
```sql
-- @keywords: your, search, terms
-- @type: file_category
-- @description: What this file does
```

**Java Files** - Add in javadoc:
```java
/**
 * @keywords your, search, terms
 * @type class_category
 * @description What this class does
 */
```

### 2. Build the Index (one command)

In VS Code Copilot chat:
```
Use the rebuild_metadata_index tool to scan my files
```

Or manually:
```bash
cd /Users/vic3custodio/projects/mcp_test_2
uv run python -c "
from trade_surveillance_mcp.metadata_index import MetadataIndex
index = MetadataIndex()
index.scan_sql_configs('path/to/your/configs')
index.scan_java_classes('path/to/your/src')
print('Index built!')
"
```

### 3. Search by Keywords

**Instead of this** ❌
```
Copilot: I need the file at /configs/reports/daily/settlement_v2.sql
```

**Do this** ✅
```
You: "Find settlement report configs"
Copilot: [Uses search_sql_configs("settlement report")]
Result: All files tagged with "settlement" + "report"
```

## 📝 Example Annotations

### SQL Config Examples

```sql
-- @keywords: trade, settlement, reconciliation, daily
-- @type: compliance_report
-- @description: Daily trade settlement reconciliation

-- @keywords: transaction, audit, investigation
-- @type: investigation_query  
-- @description: Transaction audit trail for investigations

-- @keywords: position, valuation, eod
-- @type: risk_report
-- @description: End-of-day position valuation report
```

### Java Class Examples

```java
/**
 * @keywords settlement, report, generator
 * @type report_generator
 * @description Generates daily settlement reports
 */
 
/**
 * @keywords trade, processor, execution
 * @type trade_processor
 * @description Processes trade execution workflows
 */
 
/**
 * @keywords audit, compliance, validator
 * @type validation_tool
 * @description Validates trades for compliance rules
 */
```

## 🎯 Choosing Good Keywords

**Think about how users will search:**

✅ **Good Keywords:**
- settlement, reconciliation, daily (specific terms)
- trade, transaction (common variations)
- audit, investigation, compliance (related concepts)

❌ **Bad Keywords:**
- report, query, script (too generic)
- v2, final, new (version info)

## 🔍 How Copilot Uses This

### Example 1: User Email
```
"Hi, I need yesterday's settlement data with failed trades"
```

**Copilot automatically:**
1. Calls `search_sql_configs("settlement failed")`
2. Finds `daily_settlement_report.sql` (keywords: settlement, reconciliation)
3. Finds `settlement_exceptions.sql` (keywords: settlement, failed)
4. Suggests which to use

### Example 2: Finding Java Code
```
You: "Which class generates compliance reports?"
```

**Copilot:**
1. Calls `search_java_code("compliance report generator")`
2. Finds all classes with those keywords
3. Shows you the matches with descriptions

## 🛠️ Quick Commands

**Test your annotations:**
```bash
# See what gets indexed
cd /Users/vic3custodio/projects/mcp_test_2
uv run python -c "
from trade_surveillance_mcp.metadata_index import MetadataIndex
index = MetadataIndex()
index.scan_sql_configs('examples/configs')
results = index.search('settlement')
for r in results:
    print(f'{r[\"file\"]}: {r[\"keywords\"]}')
"
```

**Check the index:**
```bash
cat metadata_index.json | jq .
```

## 📚 See Full Guide

Read [METADATA_GUIDE.md](METADATA_GUIDE.md) for:
- Complete annotation format
- Best practices
- Troubleshooting
- Advanced usage

## ✨ Benefits

- 🚀 **Fast** - Instant keyword search vs scanning file contents
- 🎯 **Accurate** - Find files by purpose, not location
- 🔄 **Flexible** - Move files around without breaking search
- 🤖 **AI-Friendly** - Copilot understands semantic search better

---

**Start annotating your first file now!** See `examples/` for templates.
