# Metadata-Based File Search Guide

This guide explains how to annotate your SQL configs and Java files so Copilot can search by **keywords** instead of file paths.

## Benefits

✅ **No more file path hunting** - Search by "settlement report" instead of remembering paths  
✅ **Semantic search** - Find files by what they do, not where they are  
✅ **Automatic indexing** - First search builds the index automatically  
✅ **Fast lookups** - Cached index for instant results  

## How to Annotate Your Files

### SQL Config Files

Add metadata comments at the top of your `.sql` files:

```sql
-- @keywords: trade, settlement, daily, reconciliation
-- @type: compliance_report
-- @description: Daily trade settlement reconciliation report for compliance

SELECT 
    t.trade_id,
    t.settlement_date,
    -- ... rest of your query
```

**Annotation format:**
- `@keywords:` - Comma-separated search terms (trade, settlement, audit, etc.)
- `@type:` - Category/type of config (compliance_report, investigation_query, etc.)
- `@description:` - Brief description of what the query does

### Java Files

Add metadata in javadoc comments at the top of your class:

```java
/**
 * Trade Settlement Report Generator
 * 
 * @keywords settlement, trade, report, daily, reconciliation
 * @type report_generator
 * @description Generates daily settlement reports by executing SQL configs
 */
public class SettlementReportGenerator {
    // ... your class implementation
}
```

**Annotation format:**
- `@keywords` - Comma-separated search terms
- `@type` - Category/type (report_generator, investigation_tool, etc.)
- `@description` - Brief description of what the class does

## How Copilot Uses Metadata

### Before (File Path Search) ❌
```
Copilot: "I need the settlement report SQL file at configs/reports/daily/settlement.sql"
You: *Have to remember exact path structure*
```

### After (Keyword Search) ✅
```
You: "I need a settlement report"
Copilot: Uses search_sql_configs("settlement report")
Result: Finds all files tagged with "settlement" keywords
```

## Example Workflow

### 1. User Email
```
From: trader@company.com
Subject: Need yesterday's settlement data

Hi, I need a report showing all failed settlements from yesterday.
Trade IDs: T12345, T12346
```

### 2. Copilot Conversation
```
You: [Paste email]

Copilot: I'll help investigate this. Let me search for settlement-related configs...

[Calls: search_sql_configs("settlement failed")]

Found:
- daily_settlement_report.sql (keywords: settlement, reconciliation, daily)
- settlement_exceptions.sql (keywords: settlement, failed, exceptions)

[Calls: search_java_code("settlement report")]

Found:
- SettlementReportGenerator.java (keywords: settlement, report, daily)

Would you like me to execute the settlement report?
```

## Best Practices

### 1. Use Descriptive Keywords
**Good:**
```sql
-- @keywords: trade, settlement, daily, reconciliation, compliance
```

**Bad:**
```sql
-- @keywords: report, data, query
```

### 2. Be Specific with Types
**Good types:**
- `compliance_report`
- `investigation_query`
- `daily_reconciliation`
- `audit_trail`

**Bad types:**
- `report`
- `query`
- `script`

### 3. Include Common Search Terms
Think about how users will search:
- "settlement" (not just "settle")
- "transaction" AND "trade" (cover both terms)
- "audit" AND "investigation" (synonyms)

### 4. Update Metadata When Changing Files
When you modify a file's purpose, update the annotations too!

## MCP Tools

### search_sql_configs
```python
search_sql_configs(
    search_keywords="settlement failed compliance"
)
```
Returns SQL configs matching those keywords.

### search_java_code
```python
search_java_code(
    search_keywords="report generator settlement"
)
```
Returns Java classes matching those keywords.

### rebuild_metadata_index
```python
rebuild_metadata_index(
    config_directory="./your/configs",
    code_directory="./your/src"
)
```
Manually rebuilds the index after adding new files.

## The Index File

The metadata is cached in `metadata_index.json`:

```json
{
  "sql_configs": {
    "daily_settlement_report.sql": {
      "keywords": ["trade", "settlement", "daily"],
      "type": "compliance_report",
      "description": "Daily trade settlement reconciliation",
      "file_path": "/path/to/file.sql"
    }
  },
  "java_classes": {
    "SettlementReportGenerator.java": {
      "keywords": ["settlement", "report", "generator"],
      "type": "report_generator",
      "methods": ["generateReport", "executeQuery"],
      "file_path": "/path/to/file.java"
    }
  }
}
```

The index is automatically created on first search. Rebuild it when you add new files.

## Examples Included

Check the `examples/` directory:
- `examples/configs/` - Annotated SQL files
- `examples/src/` - Annotated Java files

Copy these patterns to your real config and code repositories!

## Next Steps

1. **Annotate existing files** - Add metadata comments to your current configs/code
2. **Test the search** - Ask Copilot to find files by keywords
3. **Rebuild index** - Run `rebuild_metadata_index` tool after annotations
4. **Update paths** - Configure your actual repo paths in `server.py`

## Troubleshooting

**Q: Search returns no results**  
A: Run `rebuild_metadata_index` to scan your files again.

**Q: Files without annotations**  
A: They won't appear in search results. Add metadata comments!

**Q: Want to update the index**  
A: Just run `rebuild_metadata_index` - it rescans everything.
