#!/usr/bin/env python3
"""
Trade Surveillance Support MCP Server

This MCP server provides tools to automate trade surveillance support workflows:
- Parse user inquiry emails
- Search relevant SQL config files and Java code
- Execute Java processes to generate reports
- Streamline user support and investigation
"""

import asyncio
import logging
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP
from .metadata_index import MetadataIndex

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("Trade Surveillance Support")

# Initialize metadata index
metadata_index = MetadataIndex()


@mcp.tool()
async def parse_email_inquiry(email_content: str) -> dict[str, Any]:
    """
    Parse a user inquiry email to extract key information for investigation.
    
    This tool analyzes email content and extracts:
    - Inquiry type (trade issue, report request, data verification, etc.)
    - Related trade IDs or account numbers
    - Time period of interest
    - Priority level
    - Required actions
    
    Args:
        email_content: The full text content of the user's inquiry email
        
    Returns:
        A dictionary containing parsed information including inquiry_type,
        trade_ids, time_period, priority, and suggested_actions
    """
    import re
    from datetime import datetime, timedelta
    
    content_lower = email_content.lower()
    
    # Extract trade IDs (common patterns: TRD123456, TRADE-123456, T-123456, #123456)
    trade_id_patterns = [
        r'\bTRD[\-_]?\d{5,10}\b',
        r'\bTRADE[\-_]?\d{5,10}\b',
        r'\bT[\-_]\d{5,10}\b',
        r'#\d{5,10}\b',
        r'\btrade\s+(?:id|number|ref)[\s:]+(\d{5,10})\b'
    ]
    trade_ids = []
    for pattern in trade_id_patterns:
        matches = re.findall(pattern, email_content, re.IGNORECASE)
        trade_ids.extend(matches)
    trade_ids = list(set(trade_ids))  # Remove duplicates
    
    # Extract account numbers (common patterns: ACC123456, ACCT-123456, Account: 123456)
    account_patterns = [
        r'\bACC(?:T)?[\-_]?\d{5,10}\b',
        r'\baccount[\s:]+(\d{5,10})\b'
    ]
    account_numbers = []
    for pattern in account_patterns:
        matches = re.findall(pattern, email_content, re.IGNORECASE)
        account_numbers.extend(matches)
    account_numbers = list(set(account_numbers))
    
    # Extract time periods (dates, ranges, relative times)
    time_period = None
    date_patterns = [
        r'\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})\b',  # MM/DD/YYYY or DD-MM-YYYY
        r'\b(\d{4}[-/]\d{1,2}[-/]\d{1,2})\b',    # YYYY-MM-DD
        r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2},?\s+\d{4}\b',
        r'\b\d{1,2}\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{4}\b'
    ]
    
    dates_found = []
    for pattern in date_patterns:
        dates_found.extend(re.findall(pattern, email_content, re.IGNORECASE))
    
    # Check for relative time references
    if 'last week' in content_lower or 'past week' in content_lower:
        time_period = "last_week"
    elif 'last month' in content_lower or 'past month' in content_lower:
        time_period = "last_month"
    elif 'yesterday' in content_lower:
        time_period = "yesterday"
    elif 'today' in content_lower or 'this morning' in content_lower:
        time_period = "today"
    elif 'last 7 days' in content_lower or 'past 7 days' in content_lower:
        time_period = "last_7_days"
    elif 'last 30 days' in content_lower or 'past 30 days' in content_lower:
        time_period = "last_30_days"
    elif dates_found:
        time_period = dates_found[0] if isinstance(dates_found[0], str) else str(dates_found[0])
    
    # Determine inquiry type based on keywords
    inquiry_type = "general_inquiry"
    inquiry_keywords = {
        "trade_issue": ["trade error", "failed trade", "trade problem", "transaction failed", "execution issue"],
        "report_request": ["generate report", "need report", "send report", "report for", "can you provide"],
        "data_verification": ["verify", "check data", "confirm", "validate", "reconcile"],
        "settlement_inquiry": ["settlement", "settle", "payment", "clearing"],
        "compliance_check": ["compliance", "audit", "regulatory", "regulation"],
        "position_inquiry": ["position", "holdings", "balance", "exposure"],
        "transaction_history": ["transaction history", "trade history", "past trades", "historical"]
    }
    
    for inq_type, keywords in inquiry_keywords.items():
        if any(keyword in content_lower for keyword in keywords):
            inquiry_type = inq_type
            break
    
    # Determine priority based on urgency indicators
    priority = "medium"
    high_priority_words = ["urgent", "asap", "immediately", "critical", "emergency", "high priority"]
    low_priority_words = ["when you can", "no rush", "low priority", "whenever"]
    
    if any(word in content_lower for word in high_priority_words):
        priority = "high"
    elif any(word in content_lower for word in low_priority_words):
        priority = "low"
    
    # Generate suggested actions based on inquiry type
    suggested_actions = []
    if inquiry_type == "report_request":
        suggested_actions = [
            "Search for relevant report config files",
            "Identify appropriate Java report generator",
            "Execute report generation",
            "Send report to requester"
        ]
    elif inquiry_type == "trade_issue":
        suggested_actions = [
            "Search trade transaction records",
            "Check for error logs",
            "Verify trade details",
            "Generate diagnostic report"
        ]
    elif inquiry_type == "data_verification":
        suggested_actions = [
            "Query relevant data sources",
            "Run reconciliation checks",
            "Generate verification report"
        ]
    elif inquiry_type == "settlement_inquiry":
        suggested_actions = [
            "Search settlement config files",
            "Check settlement status",
            "Generate settlement report"
        ]
    elif inquiry_type == "compliance_check":
        suggested_actions = [
            "Search compliance config files",
            "Run audit checks",
            "Generate compliance report"
        ]
    else:
        suggested_actions = [
            "Analyze inquiry details",
            "Search for relevant config files",
            "Identify appropriate action"
        ]
    
    result = {
        "status": "parsed",
        "inquiry_type": inquiry_type,
        "trade_ids": trade_ids,
        "account_numbers": account_numbers,
        "time_period": time_period,
        "priority": priority,
        "suggested_actions": suggested_actions,
        "raw_content_preview": email_content[:300] + "..." if len(email_content) > 300 else email_content,
        "content_length": len(email_content)
    }
    
    logger.info(f"Parsed email inquiry: {inquiry_type}, Priority: {priority}, Found {len(trade_ids)} trade IDs")
    return result


@mcp.tool()
async def search_sql_configs(
    search_keywords: str,
    config_directory: str = "./configs"
) -> dict[str, Any]:
    """
    Search for SQL configuration files using metadata keywords instead of file paths.
    
    This tool searches through indexed SQL config files by their metadata annotations.
    Files should include metadata comments like:
    
    -- @keywords: trade, transaction, daily_report
    -- @type: compliance_check
    -- @description: Daily trade reconciliation report
    
    Args:
        search_keywords: Keywords to search for (e.g., "trade settlement", "compliance", "daily report")
        config_directory: Path to the directory containing SQL config files (used for initial scan)
        
    Returns:
        A dictionary containing matching config files with their metadata
    """
    logger.info(f"Searching SQL configs for keywords: {search_keywords}")
    
    # Scan directory if index is empty
    if not metadata_index.index.get("sql_configs"):
        logger.info(f"Scanning SQL configs in: {config_directory}")
        metadata_index.scan_sql_configs(config_directory)
    
    # Search by keywords
    matches = metadata_index.search(search_keywords, file_type="sql")
    
    result = {
        "status": "success",
        "search_keywords": search_keywords,
        "matches_found": len(matches),
        "config_files": matches
    }
    
    logger.info(f"Found {len(matches)} SQL config matches")
    return result


@mcp.tool()
async def search_java_code(
    search_keywords: str,
    code_directory: str = "./src"
) -> dict[str, Any]:
    """
    Search for Java classes using metadata keywords instead of file paths.
    
    This tool searches through indexed Java files by their javadoc metadata annotations.
    Java classes should include metadata in javadoc comments like:
    
    /**
     * @keywords trade, settlement, report_generator
     * @type report_engine
     * @description Generates daily settlement reports
     */
    
    Args:
        search_keywords: Keywords to search for (e.g., "report generator", "trade processor")
        code_directory: Path to the directory containing Java source files (used for initial scan)
        
    Returns:
        A dictionary containing matching Java files with their metadata and methods
    """
    logger.info(f"Searching Java code for keywords: {search_keywords}")
    
    # Scan directory if index is empty
    if not metadata_index.index.get("java_classes"):
        logger.info(f"Scanning Java classes in: {code_directory}")
        metadata_index.scan_java_classes(code_directory)
    
    # Search by keywords
    matches = metadata_index.search(search_keywords, file_type="java")
    
    result = {
        "status": "success",
        "search_keywords": search_keywords,
        "matches_found": len(matches),
        "java_classes": matches
    }
    
    logger.info(f"Found {len(matches)} Java class matches")
    return result


@mcp.tool()
async def execute_java_report(
    java_class: str,
    config_file: str,
    output_directory: str = "./reports"
) -> dict[str, Any]:
    """
    Execute a Java unit test to generate a trade surveillance report.
    
    This tool runs the unit test for the specified Java class with the given 
    config file to generate the required report or data extract. Running tests
    ensures the report generation is validated during execution.
    
    Args:
        java_class: The fully qualified Java class name (e.g., "com.trade.SettlementReportGenerator")
        config_file: Path to the SQL config file to use
        output_directory: Directory where the report should be saved
        
    Returns:
        A dictionary containing execution status, report path, and any errors
    """
    import subprocess
    import os
    from datetime import datetime
    from pathlib import Path
    
    start_time = datetime.now()
    
    # Derive test class name (e.g., SettlementReportGenerator -> SettlementReportGeneratorTest)
    class_simple_name = java_class.split('.')[-1]
    test_class_name = f"{class_simple_name}Test"
    
    # Get the package path from the java_class
    if '.' in java_class:
        package_parts = java_class.rsplit('.', 1)[0]
        test_class_full = f"{package_parts}.{test_class_name}"
    else:
        test_class_full = test_class_name
    
    # Create output directory if it doesn't exist
    output_path = Path(output_directory)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Generate report filename based on config and timestamp
    config_name = Path(config_file).stem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"{config_name}_report_{timestamp}.csv"
    report_path = output_path / report_filename
    
    result = {
        "status": "running",
        "java_class": java_class,
        "test_class": test_class_full,
        "config_file": config_file,
        "output_directory": str(output_directory),
        "report_path": str(report_path),
        "execution_time": None,
        "errors": [],
        "test_output": None
    }
    
    try:
        logger.info(f"Executing Java test: {test_class_full} for class: {java_class}")
        
        # Set environment variables for the test to use
        env = os.environ.copy()
        env['CONFIG_FILE'] = str(Path(config_file).absolute())
        env['OUTPUT_FILE'] = str(report_path.absolute())
        
        # Determine build tool (Maven or Gradle)
        project_root = Path.cwd()
        has_maven = (project_root / "pom.xml").exists()
        has_gradle = (project_root / "build.gradle").exists() or (project_root / "build.gradle.kts").exists()
        
        if has_maven:
            # Run Maven test for specific test class
            cmd = [
                "mvn",
                "test",
                f"-Dtest={test_class_name}",
                f"-DconfigFile={config_file}",
                f"-DoutputFile={report_path}"
            ]
            logger.info(f"Running Maven command: {' '.join(cmd)}")
        elif has_gradle:
            # Run Gradle test for specific test class
            cmd = [
                "./gradlew",
                "test",
                f"--tests {test_class_name}",
                f"-DconfigFile={config_file}",
                f"-DoutputFile={report_path}"
            ]
            logger.info(f"Running Gradle command: {' '.join(cmd)}")
        else:
            # Fallback to direct JUnit execution
            cmd = [
                "java",
                "-cp",
                "target/test-classes:target/classes:lib/*",  # Adjust classpath as needed
                "org.junit.runner.JUnitCore",
                test_class_full
            ]
            logger.info(f"Running JUnit command: {' '.join(cmd)}")
        
        # Execute the test
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
            cwd=str(project_root)
        )
        
        stdout, stderr = await process.communicate()
        
        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()
        result["execution_time"] = f"{execution_time:.2f}s"
        
        # Process output
        stdout_text = stdout.decode('utf-8') if stdout else ""
        stderr_text = stderr.decode('utf-8') if stderr else ""
        
        result["test_output"] = stdout_text
        
        if process.returncode == 0:
            result["status"] = "success"
            logger.info(f"Test execution completed successfully in {execution_time:.2f}s")
            
            # Verify report was created
            if report_path.exists():
                file_size = report_path.stat().st_size
                result["report_size"] = f"{file_size} bytes"
                logger.info(f"Report generated: {report_path} ({file_size} bytes)")
            else:
                result["status"] = "completed_no_output"
                result["errors"].append("Test passed but report file was not created")
                logger.warning("Test passed but no report file found")
        else:
            result["status"] = "failed"
            result["errors"].append(f"Test execution failed with exit code {process.returncode}")
            if stderr_text:
                result["errors"].append(stderr_text)
            logger.error(f"Test execution failed: {stderr_text}")
        
    except FileNotFoundError as e:
        result["status"] = "error"
        result["errors"].append(f"Build tool not found: {str(e)}")
        result["errors"].append("Ensure Maven (mvn) or Gradle (./gradlew) is installed and in PATH")
        logger.error(f"Build tool not found: {e}")
    except Exception as e:
        result["status"] = "error"
        result["errors"].append(f"Unexpected error: {str(e)}")
        logger.error(f"Unexpected error during test execution: {e}", exc_info=True)
    
    return result


@mcp.tool()
async def rebuild_metadata_index(
    config_directory: str = "./configs",
    code_directory: str = "./src"
) -> dict[str, Any]:
    """
    Rebuild the metadata index by scanning all SQL configs and Java files.
    
    Use this tool when you've added new files or updated metadata annotations.
    The index is automatically built on first search, but you can manually rebuild
    it with this tool.
    
    Args:
        config_directory: Path to the directory containing SQL config files
        code_directory: Path to the directory containing Java source files
        
    Returns:
        A summary of the indexing operation
    """
    logger.info("Rebuilding metadata index...")
    
    sql_count = len(metadata_index.scan_sql_configs(config_directory))
    java_count = len(metadata_index.scan_java_classes(code_directory))
    
    result = {
        "status": "success",
        "sql_configs_indexed": sql_count,
        "java_classes_indexed": java_count,
        "total_files_indexed": sql_count + java_count,
        "index_file": str(metadata_index.index_file.absolute())
    }
    
    logger.info(f"Index rebuilt: {sql_count} SQL configs, {java_count} Java classes")
    return result


@mcp.tool()
async def generate_response_summary(
    parsed_email: dict[str, Any],
    config_files: list[str],
    report_path: str
) -> str:
    """
    Generate a summary response for the user inquiry with all relevant information.
    
    This tool combines all the gathered information into a clear, actionable
    response that can be sent back to the user.
    
    Args:
        parsed_email: The parsed email inquiry data
        config_files: List of config files that were used
        report_path: Path to the generated report file
        
    Returns:
        A formatted summary string ready to send to the user
    """
    summary = f"""
Trade Surveillance Support - Response Summary
==============================================

Inquiry Type: {parsed_email.get('inquiry_type', 'Unknown')}
Priority: {parsed_email.get('priority', 'Medium')}

Actions Taken:
- Analyzed inquiry email
- Located {len(config_files)} relevant configuration files
- Generated report: {report_path}

Next Steps:
{chr(10).join(f"- {action}" for action in parsed_email.get('suggested_actions', []))}

Report Location: {report_path}

Please review the generated report and let me know if you need any additional information.
"""
    
    logger.info("Generated response summary")
    return summary.strip()


def main():
    """
    Main entry point for the Trade Surveillance MCP server.
    """
    logger.info("Starting Trade Surveillance MCP Server...")
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
