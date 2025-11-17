"""
Metadata indexer for SQL configs and Java code.

This module provides functionality to index files with metadata annotations
so Copilot can search by keywords instead of file paths.
"""

import json
import re
from pathlib import Path
from typing import Any


class MetadataIndex:
    """Index for searching files by metadata keywords instead of paths."""
    
    def __init__(self, index_file: str = "metadata_index.json"):
        self.index_file = Path(index_file)
        self.index: dict[str, Any] = self._load_index()
    
    def _load_index(self) -> dict[str, Any]:
        """Load the metadata index from file."""
        if self.index_file.exists():
            with open(self.index_file, 'r') as f:
                return json.load(f)
        return {"sql_configs": {}, "java_classes": {}}
    
    def _save_index(self):
        """Save the metadata index to file."""
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=2)
    
    def scan_sql_configs(self, config_dir: str) -> dict[str, Any]:
        """
        Scan SQL config files and extract metadata from comments.
        
        Looks for annotations like:
        -- @keywords: trade, transaction, daily_report
        -- @type: compliance_check
        -- @description: Daily trade reconciliation report
        """
        config_path = Path(config_dir)
        if not config_path.exists():
            return {}
        
        configs = {}
        for sql_file in config_path.rglob("*.sql"):
            metadata = self._extract_sql_metadata(sql_file)
            if metadata:
                configs[str(sql_file.relative_to(config_path))] = metadata
        
        self.index["sql_configs"] = configs
        self._save_index()
        return configs
    
    def _extract_sql_metadata(self, file_path: Path) -> dict[str, Any]:
        """Extract metadata from SQL file comments."""
        metadata = {
            "file_path": str(file_path),
            "file_name": file_path.name,
            "keywords": [],
            "type": None,
            "description": None
        }
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Extract @keywords
            keywords_match = re.search(r'--\s*@keywords:\s*([^\n]+)', content, re.IGNORECASE)
            if keywords_match:
                keywords = [k.strip() for k in keywords_match.group(1).split(',')]
                metadata["keywords"] = keywords
            
            # Extract @type
            type_match = re.search(r'--\s*@type:\s*([^\n]+)', content, re.IGNORECASE)
            if type_match:
                metadata["type"] = type_match.group(1).strip()
            
            # Extract @description
            desc_match = re.search(r'--\s*@description:\s*([^\n]+)', content, re.IGNORECASE)
            if desc_match:
                metadata["description"] = desc_match.group(1).strip()
            
            return metadata if metadata["keywords"] or metadata["type"] else None
        except Exception:
            return None
    
    def scan_java_classes(self, code_dir: str) -> dict[str, Any]:
        """
        Scan Java files and extract metadata from javadoc comments.
        
        Looks for annotations like:
        /**
         * @keywords trade, settlement, report_generator
         * @type report_engine
         * @description Generates daily settlement reports
         */
        """
        code_path = Path(code_dir)
        if not code_path.exists():
            return {}
        
        classes = {}
        for java_file in code_path.rglob("*.java"):
            metadata = self._extract_java_metadata(java_file)
            if metadata:
                classes[str(java_file.relative_to(code_path))] = metadata
        
        self.index["java_classes"] = classes
        self._save_index()
        return classes
    
    def _extract_java_metadata(self, file_path: Path) -> dict[str, Any]:
        """Extract metadata from Java file javadoc comments."""
        metadata = {
            "file_path": str(file_path),
            "file_name": file_path.name,
            "class_name": file_path.stem,
            "keywords": [],
            "type": None,
            "description": None,
            "methods": []
        }
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Extract @keywords
            keywords_match = re.search(r'\*\s*@keywords[:\s]+([^\n]+)', content, re.IGNORECASE)
            if keywords_match:
                keywords = [k.strip() for k in keywords_match.group(1).split(',')]
                metadata["keywords"] = keywords
            
            # Extract @type
            type_match = re.search(r'\*\s*@type[:\s]+([^\n]+)', content, re.IGNORECASE)
            if type_match:
                metadata["type"] = type_match.group(1).strip()
            
            # Extract @description
            desc_match = re.search(r'\*\s*@description[:\s]+([^\n]+)', content, re.IGNORECASE)
            if desc_match:
                metadata["description"] = desc_match.group(1).strip()
            
            # Extract public methods
            method_pattern = r'public\s+(?:static\s+)?[\w<>\[\]]+\s+(\w+)\s*\('
            methods = re.findall(method_pattern, content)
            metadata["methods"] = methods
            
            return metadata if metadata["keywords"] or metadata["type"] else None
        except Exception:
            return None
    
    def search(self, query: str, file_type: str = "all") -> list[dict[str, Any]]:
        """
        Search the index by keywords, type, or description.
        
        Args:
            query: Search terms (space or comma separated)
            file_type: "sql", "java", or "all"
        
        Returns:
            List of matching files with their metadata
        """
        query_terms = [term.strip().lower() for term in re.split(r'[,\s]+', query)]
        results = []
        
        # Search SQL configs
        if file_type in ("sql", "all"):
            for file_name, metadata in self.index.get("sql_configs", {}).items():
                if self._matches_query(metadata, query_terms):
                    results.append({
                        "type": "sql_config",
                        "file": file_name,
                        **metadata
                    })
        
        # Search Java classes
        if file_type in ("java", "all"):
            for file_name, metadata in self.index.get("java_classes", {}).items():
                if self._matches_query(metadata, query_terms):
                    results.append({
                        "type": "java_class",
                        "file": file_name,
                        **metadata
                    })
        
        return results
    
    def _matches_query(self, metadata: dict[str, Any], query_terms: list[str]) -> bool:
        """Check if metadata matches any query terms."""
        # Combine all searchable fields
        searchable = " ".join([
            " ".join(metadata.get("keywords", [])),
            metadata.get("type", ""),
            metadata.get("description", ""),
            metadata.get("file_name", "")
        ]).lower()
        
        # Match if any query term is found
        return any(term in searchable for term in query_terms)
