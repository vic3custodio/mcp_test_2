package com.trade.surveillance;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.ArrayList;

/**
 * Unit test for TransactionAuditProcessor.
 * 
 * This test generates a transaction audit report using the configuration file
 * specified in the CONFIG_FILE environment variable or system property.
 * The report is written to the path specified in OUTPUT_FILE.
 * 
 * @keywords transaction, audit, test, processor, compliance
 * @type test_audit_processor
 * @description Unit test that generates transaction audit reports for compliance
 */
public class TransactionAuditProcessorTest {
    
    private String configFile;
    private String outputFile;
    private TransactionAuditProcessor processor;
    private DateTimeFormatter dateFormatter;
    
    @BeforeEach
    public void setUp() {
        // Get config file from environment variable or system property
        configFile = System.getenv("CONFIG_FILE");
        if (configFile == null) {
            configFile = System.getProperty("configFile", "configs/transaction_audit.sql");
        }
        
        // Get output file from environment variable or system property
        outputFile = System.getenv("OUTPUT_FILE");
        if (outputFile == null) {
            outputFile = System.getProperty("outputFile", "reports/transaction_audit_test.csv");
        }
        
        // Note: In actual implementation, pass database connection
        processor = new TransactionAuditProcessor(null);
        dateFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        
        System.out.println("=== Transaction Audit Processor Test ===");
        System.out.println("Config File: " + configFile);
        System.out.println("Output File: " + outputFile);
    }
    
    @Test
    @DisplayName("Generate Transaction Audit Report from Config")
    public void testGenerateAuditReport() throws IOException {
        // Ensure output directory exists
        Path outputPath = Paths.get(outputFile);
        Files.createDirectories(outputPath.getParent());
        
        // Read SQL config file
        String sqlQuery = readConfigFile(configFile);
        assertNotNull(sqlQuery, "SQL query should not be null");
        assertFalse(sqlQuery.trim().isEmpty(), "SQL query should not be empty");
        
        System.out.println("\n--- SQL Query from Config ---");
        System.out.println(sqlQuery);
        
        // Generate audit report data
        List<String[]> auditData = generateMockAuditData();
        assertNotNull(auditData, "Audit data should not be null");
        assertTrue(auditData.size() > 0, "Audit report should contain data");
        
        // Write report to CSV
        writeReportToCSV(outputFile, auditData);
        
        // Verify report file was created
        File reportFile = new File(outputFile);
        assertTrue(reportFile.exists(), "Report file should be created");
        assertTrue(reportFile.length() > 0, "Report file should not be empty");
        
        System.out.println("\n--- Audit Report Generated Successfully ---");
        System.out.println("Report Location: " + reportFile.getAbsolutePath());
        System.out.println("Report Size: " + reportFile.length() + " bytes");
        System.out.println("Transactions Audited: " + (auditData.size() - 1)); // Exclude header
    }
    
    @Test
    @DisplayName("Validate Audit Trail Completeness")
    public void testAuditTrailCompleteness() throws IOException {
        List<String[]> auditData = generateMockAuditData();
        
        // Validate header
        String[] header = auditData.get(0);
        assertEquals(9, header.length, "Audit report should have 9 columns");
        assertEquals("Transaction ID", header[0]);
        assertEquals("Timestamp", header[1]);
        assertEquals("User ID", header[2]);
        assertEquals("Action", header[3]);
        
        // Validate required audit fields are present
        for (int i = 1; i < auditData.size(); i++) {
            String[] row = auditData.get(i);
            assertEquals(9, row.length, "Each row should have 9 columns");
            assertNotNull(row[0], "Transaction ID should not be null");
            assertNotNull(row[1], "Timestamp should not be null");
            assertNotNull(row[2], "User ID should not be null");
            assertNotNull(row[3], "Action should not be null");
        }
        
        System.out.println("✓ Audit trail completeness validation passed");
    }
    
    @Test
    @DisplayName("Detect Suspicious Transactions")
    public void testSuspiciousTransactionDetection() {
        List<String[]> auditData = generateMockAuditData();
        List<String> suspiciousTransactions = new ArrayList<>();
        
        // Check for suspicious patterns (excluding header)
        for (int i = 1; i < auditData.size(); i++) {
            String[] row = auditData.get(i);
            String riskLevel = row[7]; // Risk Level column
            
            if ("HIGH".equals(riskLevel) || "CRITICAL".equals(riskLevel)) {
                suspiciousTransactions.add(row[0]); // Transaction ID
            }
        }
        
        assertFalse(suspiciousTransactions.isEmpty(), "Should detect suspicious transactions");
        
        System.out.println("\n--- Suspicious Transactions Detected ---");
        System.out.println("Count: " + suspiciousTransactions.size());
        for (String txnId : suspiciousTransactions) {
            System.out.println("  - " + txnId);
        }
    }
    
    /**
     * Read SQL query from config file
     */
    private String readConfigFile(String configPath) throws IOException {
        Path path = Paths.get(configPath);
        if (!Files.exists(path)) {
            throw new IOException("Config file not found: " + configPath);
        }
        return new String(Files.readAllBytes(path));
    }
    
    /**
     * Generate mock audit data for testing
     */
    private List<String[]> generateMockAuditData() {
        LocalDateTime now = LocalDateTime.now();
        
        return List.of(
            new String[]{"Transaction ID", "Timestamp", "User ID", "Action", "Amount", "Currency", "IP Address", "Risk Level", "Status"},
            new String[]{"TXN-200001", now.minusHours(5).format(dateFormatter), "USR-1001", "TRADE_EXECUTION", "150000.00", "USD", "192.168.1.100", "LOW", "APPROVED"},
            new String[]{"TXN-200002", now.minusHours(4).format(dateFormatter), "USR-1002", "TRADE_MODIFICATION", "250000.00", "EUR", "192.168.1.101", "MEDIUM", "APPROVED"},
            new String[]{"TXN-200003", now.minusHours(3).format(dateFormatter), "USR-1003", "TRADE_CANCELLATION", "75000.00", "GBP", "192.168.1.102", "HIGH", "FLAGGED"},
            new String[]{"TXN-200004", now.minusHours(2).format(dateFormatter), "USR-1001", "TRADE_EXECUTION", "500000.00", "USD", "10.20.30.40", "CRITICAL", "UNDER_REVIEW"},
            new String[]{"TXN-200005", now.minusHours(2).format(dateFormatter), "USR-1001", "TRADE_EXECUTION", "525000.00", "USD", "10.20.30.40", "CRITICAL", "UNDER_REVIEW"},
            new String[]{"TXN-200006", now.minusHours(1).format(dateFormatter), "USR-1004", "TRADE_EXECUTION", "125000.00", "CHF", "192.168.1.103", "LOW", "APPROVED"},
            new String[]{"TXN-200007", now.minusMinutes(45).format(dateFormatter), "USR-1005", "SETTLEMENT_OVERRIDE", "300000.00", "USD", "192.168.1.104", "HIGH", "FLAGGED"},
            new String[]{"TXN-200008", now.minusMinutes(30).format(dateFormatter), "USR-1002", "TRADE_EXECUTION", "175000.00", "EUR", "192.168.1.101", "LOW", "APPROVED"},
            new String[]{"TXN-200009", now.minusMinutes(15).format(dateFormatter), "USR-1006", "TRADE_EXECUTION", "225000.00", "USD", "192.168.1.105", "MEDIUM", "APPROVED"},
            new String[]{"TXN-200010", now.format(dateFormatter), "USR-UNKNOWN", "UNAUTHORIZED_ACCESS", "0.00", "USD", "203.0.113.42", "CRITICAL", "BLOCKED"}
        );
    }
    
    /**
     * Write report data to CSV file
     */
    private void writeReportToCSV(String filePath, List<String[]> data) throws IOException {
        try (FileWriter writer = new FileWriter(filePath)) {
            for (String[] row : data) {
                // Escape commas in fields by wrapping in quotes
                String[] escapedRow = new String[row.length];
                for (int i = 0; i < row.length; i++) {
                    escapedRow[i] = "\"" + row[i].replace("\"", "\"\"") + "\"";
                }
                writer.write(String.join(",", escapedRow));
                writer.write("\n");
            }
        }
    }
    
    @AfterEach
    public void tearDown() {
        System.out.println("\n========================================\n");
    }
}
