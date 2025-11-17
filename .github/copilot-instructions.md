# Trade Surveillance Support MCP Server

## Project Overview
This is a Model Context Protocol (MCP) server designed to automate trade surveillance support workflows by:
- Parsing user inquiry emails
- Searching relevant SQL config files and Java code
- Executing Java processes to generate reports
- Streamlining user support and investigation

## Implementation Details
- **Language**: Python 3.10+
- **Framework**: MCP SDK with FastMCP
- **Transport**: STDIO (for local execution)
- **Package Manager**: uv (recommended)

## Architecture
- **MCP Server** (`trade_surveillance_mcp/server.py`): Provides custom tools to VS Code Copilot
- **Email Parser**: Extracts key information from user inquiries
- **Config Searcher**: Finds relevant SQL and config files in your repository
- **Code Searcher**: Locates Java classes and methods for report generation
- **Java Executor**: Runs Java code to generate reports
- **Response Generator**: Formats comprehensive summaries

## Available MCP Tools

### 1. parse_email_inquiry
Analyzes email content to extract inquiry type, trade IDs, time periods, priority, and suggested actions.

### 2. search_sql_configs (⭐ Metadata-based)
Searches through SQL configuration files by **keywords** instead of file paths. Files must have metadata annotations:
```sql
-- @keywords: settlement, trade, daily
-- @type: compliance_report
-- @description: Daily settlement report
```

### 3. search_java_code (⭐ Metadata-based)
Locates Java source files by **keywords** instead of file paths. Classes must have javadoc annotations:
```java
/**
 * @keywords report, generator, settlement
 * @type report_generator
 */
```

### 4. execute_java_report
Executes Java processes with specified config files to generate reports.

### 5. rebuild_metadata_index
Rebuilds the search index by scanning all annotated files. Use after adding new files or updating annotations.

### 6. generate_response_summary
Creates comprehensive response summaries combining all gathered information.

## Usage with VS Code Copilot

1. **Start a chat**: Open Copilot chat in VS Code
2. **Paste user email**: Copy and paste the support inquiry email
3. **Let Copilot work**: It will automatically:
   - Parse the email using `parse_email_inquiry`
   - Search for relevant configs with `search_sql_configs`
   - Find Java code with `search_java_code`
   - Execute reports with `execute_java_report`
   - Generate a summary with `generate_response_summary`

Example prompt:
```
I received this email from a trader asking about their transactions from last week:

[Email content here]

Can you help me investigate and generate the necessary reports?
```

## Development Guidelines
- Follow MCP SDK best practices
- Implement async functions for all tools
- Use proper logging for debugging
- Handle errors gracefully with clear messages
- Update search paths to match your repository structure

## Customization Required

Before using in production, customize these areas:

1. **Repository Paths**: Update default directories in tool functions
2. **Email Parsing**: Implement NLP or regex patterns for your email format
3. **File Search**: Add actual file searching logic (grep, ripgrep, etc.)
4. **Java Execution**: Configure Java classpath and execution parameters
5. **Config Format**: Adapt to your SQL config file format

## Status
✓ Project setup complete
✓ MCP server implemented with 5 tools
✓ Dependencies installed and tested
✓ VS Code configuration ready

**Next Steps**: Customize paths and implement actual search/execution logic for your environment.
