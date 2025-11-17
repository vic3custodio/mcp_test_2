# Trade Surveillance Support MCP Server

An MCP (Model Context Protocol) server designed to automate trade surveillance support workflows by integrating with your existing SQL configs and Java code repositories.

## Overview

This MCP server enables you to:
- **Parse user inquiry emails** - Extract key information from support emails automatically
- **Search SQL config files** - Find relevant database queries and configurations
- **Search Java code** - Locate report generation classes and methods
- **Execute Java reports** - Run Java processes to generate data and reports
- **Generate response summaries** - Create comprehensive responses for user inquiries

## Installation

### Prerequisites
- Python 3.10 or higher
- `uv` package manager (recommended) or `pip`

### Install with uv (recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install the MCP server
uv pip install -e .
```

### Install with pip

```bash
pip install -e .
```

## Configuration

### Setting up with VS Code

1. Open VS Code Settings
2. Search for "MCP"
3. Add a new MCP server configuration:

```json
{
  "mcp.servers": {
    "trade-surveillance": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/mcp_test_2",
        "run",
        "trade-surveillance-mcp"
      ]
    }
  }
}
```

### Setting up with Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "trade-surveillance": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/mcp_test_2",
        "run",
        "trade-surveillance-mcp"
      ]
    }
  }
}
```

**macOS/Linux:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

## 🎯 Keyword-Based Search (No File Paths!)

Instead of searching by file paths, this MCP server uses **metadata annotations** so Copilot can find files by what they do:

**Example SQL annotation:**
```sql
-- @keywords: trade, settlement, daily, reconciliation
-- @type: compliance_report
-- @description: Daily trade settlement reconciliation report
```

**Example Java annotation:**
```java
/**
 * @keywords settlement, report, generator
 * @type report_generator
 * @description Generates daily settlement reports
 */
```

**Result:** Copilot searches by keywords like "settlement report" instead of file paths! 

📚 **Documentation:**
- [QUICKSTART.md](QUICKSTART.md) - Get started in 5 minutes
- [METADATA_GUIDE.md](METADATA_GUIDE.md) - Complete annotation guide
- `examples/` - Annotated SQL and Java examples

## Usage

### With GitHub Copilot in VS Code

1. Open a chat with Copilot
2. Paste a user inquiry email
3. Copilot will automatically use the MCP tools to:
   - Parse the email
   - Search for relevant configs **by keywords** (not file paths!)
   - Search for Java code **by keywords**
   - Execute reports
   - Generate a response

Example prompt:
```
I received this email from a user:

[Paste email content here]

Can you help me investigate and generate the necessary reports?
```

### Available Tools

#### 1. `parse_email_inquiry`
Extracts key information from user inquiry emails including inquiry type, trade IDs, time periods, and priority.

#### 2. `search_sql_configs` ⭐ **Metadata-based search**
Searches through your SQL configuration files by **keywords** instead of file paths. Files are searched using metadata annotations (see METADATA_GUIDE.md).

#### 3. `search_java_code` ⭐ **Metadata-based search**
Locates Java classes and methods by **keywords** instead of file paths. Classes are found using javadoc annotations (see METADATA_GUIDE.md).

#### 4. `execute_java_report`
Runs Java processes with the appropriate config files to generate reports.

#### 5. `rebuild_metadata_index`
Rebuilds the search index by scanning all annotated SQL configs and Java files. Run this after adding new files or updating annotations.

#### 6. `generate_response_summary`
Creates a comprehensive summary response for the user.

## Project Structure

```
mcp_test_2/
├── trade_surveillance_mcp/
│   ├── __init__.py
│   └── server.py          # Main MCP server implementation
├── pyproject.toml          # Project dependencies
├── README.md
└── .github/
    └── copilot-instructions.md
```

## Development

### Running Locally

```bash
# Run the server directly
uv run trade-surveillance-mcp

# Or with Python
python -m trade_surveillance_mcp.server
```

### Customization

You'll need to customize the server to work with your specific repository structure:

1. **Update search paths** - Modify `config_directory` and `code_directory` parameters
2. **Implement email parsing** - Add your email parsing logic in `parse_email_inquiry`
3. **Add file search** - Implement actual file searching in `search_sql_configs` and `search_java_code`
4. **Configure Java execution** - Add your Java classpath and execution logic in `execute_java_report`

### Connecting to Your Repository

Point the MCP server to your actual config and code repositories:

```python
# Example: Update default directories
@mcp.tool()
async def search_sql_configs(
    search_term: str,
    config_directory: str = "/path/to/your/sql/configs"
):
    # Your implementation
```

## Next Steps

1. ✅ **MCP server is ready!** - Restart VS Code to load it
2. 📝 **Annotate your files** - Add metadata keywords to your SQL configs and Java code ([QUICKSTART.md](QUICKSTART.md))
3. 🔍 **Build the index** - Use `rebuild_metadata_index` tool in Copilot
4. ⚙️ **Customize paths** - Update default directories in `server.py` to your repos
5. 🎯 **Test with Copilot** - Paste a user email and let Copilot search by keywords!

### Key Innovation: No More File Path Search! 🎉

Your SQL configs and Java files are now **searchable by keywords**:
- Copilot finds files by what they do, not where they are
- Search "settlement report" instead of remembering `configs/reports/daily/settlement_v2.sql`
- See examples in `examples/configs/` and `examples/src/`

## Troubleshooting

### Server not appearing in VS Code
- Check the MCP server logs in VS Code Output panel
- Verify the absolute path in configuration is correct
- Ensure `uv` is installed and in PATH

### Python version issues
- Ensure Python 3.10+ is installed: `python --version`
- Use `uv` for better environment management

### Java execution errors
- Verify Java is installed: `java -version`
- Check classpath configuration
- Ensure config files are accessible

## Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [FastMCP Documentation](https://github.com/modelcontextprotocol/python-sdk)
- [VS Code MCP Integration](https://code.visualstudio.com/docs/copilot/chat/mcp)

## License

MIT
