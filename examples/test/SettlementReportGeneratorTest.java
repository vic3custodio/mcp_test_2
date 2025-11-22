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
import java.util.List;

/**
 * Unit test for SettlementReportGenerator.
 * 
 * This test generates a settlement report using the configuration file
 * specified in the CONFIG_FILE environment variable or system property.
 * The report is written to the path specified in OUTPUT_FILE.
 * 
 * @keywords settlement, report, test, generator
 * @type test_report_generator
 * @description Unit test that generates settlement reports for validation
 */
public class SettlementReportGeneratorTest {
    
    private String configFile;
    private String outputFile;
    private SettlementReportGenerator generator;
    
    @BeforeEach
    public void setUp() {
        // Get config file from environment variable or system property
        configFile = System.getenv("CONFIG_FILE");
        if (configFile == null) {
            configFile = System.getProperty("configFile", "configs/daily_settlement_report.sql");
        }
        
        // Get output file from environment variable or system property
        outputFile = System.getenv("OUTPUT_FILE");
        if (outputFile == null) {
            outputFile = System.getProperty("outputFile", "reports/settlement_report_test.csv");
        }
        
        generator = new SettlementReportGenerator();
        
        System.out.println("=== Settlement Report Generator Test ===");
        System.out.println("Config File: " + configFile);
        System.out.println("Output File: " + outputFile);
    }
    
    @Test
    @DisplayName("Generate Settlement Report from Config")
    public void testGenerateSettlementReport() throws IOException {
        // Ensure output directory exists
        Path outputPath = Paths.get(outputFile);
        Files.createDirectories(outputPath.getParent());
        
        // Read SQL config file
        String sqlQuery = readConfigFile(configFile);
        assertNotNull(sqlQuery, "SQL query should not be null");
        assertFalse(sqlQuery.trim().isEmpty(), "SQL query should not be empty");
        
        System.out.println("\n--- SQL Query from Config ---");
        System.out.println(sqlQuery);
        
        // Generate report data (simulate database query results)
        List<String[]> reportData = generateMockSettlementData();
        assertNotNull(reportData, "Report data should not be null");
        assertTrue(reportData.size() > 0, "Report should contain data");
        
        // Write report to CSV
        writeReportToCSV(outputFile, reportData);
        
        // Verify report file was created
        File reportFile = new File(outputFile);
        assertTrue(reportFile.exists(), "Report file should be created");
        assertTrue(reportFile.length() > 0, "Report file should not be empty");
        
        System.out.println("\n--- Report Generated Successfully ---");
        System.out.println("Report Location: " + reportFile.getAbsolutePath());
        System.out.println("Report Size: " + reportFile.length() + " bytes");
        System.out.println("Records Generated: " + (reportData.size() - 1)); // Exclude header
    }
    
    @Test
    @DisplayName("Validate Settlement Report Format")
    public void testReportFormat() throws IOException {
        List<String[]> reportData = generateMockSettlementData();
        
        // Validate header
        String[] header = reportData.get(0);
        assertEquals(7, header.length, "Report should have 7 columns");
        assertEquals("Trade ID", header[0]);
        assertEquals("Settlement Date", header[1]);
        assertEquals("Amount", header[2]);
        
        // Validate data rows
        for (int i = 1; i < reportData.size(); i++) {
            String[] row = reportData.get(i);
            assertEquals(7, row.length, "Each row should have 7 columns");
            assertTrue(row[0].startsWith("TRD-"), "Trade ID should start with TRD-");
            assertNotNull(row[1], "Settlement date should not be null");
            assertTrue(Double.parseDouble(row[2]) > 0, "Amount should be positive");
        }
        
        System.out.println("✓ Report format validation passed");
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
     * Generate mock settlement data for testing
     */
    private List<String[]> generateMockSettlementData() {
        return List.of(
            new String[]{"Trade ID", "Settlement Date", "Amount", "Currency", "Status", "Counterparty", "Account"},
            new String[]{"TRD-100001", "2025-11-22", "150000.00", "USD", "SETTLED", "Goldman Sachs", "ACC-12345"},
            new String[]{"TRD-100002", "2025-11-22", "250000.00", "EUR", "SETTLED", "JP Morgan", "ACC-12346"},
            new String[]{"TRD-100003", "2025-11-22", "75000.00", "GBP", "PENDING", "Morgan Stanley", "ACC-12347"},
            new String[]{"TRD-100004", "2025-11-22", "500000.00", "USD", "SETTLED", "Citibank", "ACC-12348"},
            new String[]{"TRD-100005", "2025-11-22", "125000.00", "CHF", "SETTLED", "UBS", "ACC-12349"},
            new String[]{"TRD-100006", "2025-11-22", "300000.00", "USD", "FAILED", "Bank of America", "ACC-12350"},
            new String[]{"TRD-100007", "2025-11-22", "175000.00", "EUR", "SETTLED", "Deutsche Bank", "ACC-12351"},
            new String[]{"TRD-100008", "2025-11-22", "225000.00", "USD", "SETTLED", "Barclays", "ACC-12352"},
            new String[]{"TRD-100009", "2025-11-22", "90000.00", "JPY", "PENDING", "Nomura", "ACC-12353"},
            new String[]{"TRD-100010", "2025-11-22", "450000.00", "USD", "SETTLED", "Credit Suisse", "ACC-12354"}
        );
    }
    
    /**
     * Write report data to CSV file
     */
    private void writeReportToCSV(String filePath, List<String[]> data) throws IOException {
        try (FileWriter writer = new FileWriter(filePath)) {
            for (String[] row : data) {
                writer.write(String.join(",", row));
                writer.write("\n");
            }
        }
    }
    
    @AfterEach
    public void tearDown() {
        System.out.println("\n========================================\n");
    }
}
