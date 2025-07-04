#!/usr/bin/env python3
"""
MCP Document Analyzer Server (stdio version)

This is a Model Context Protocol (MCP) server that provides document analysis capabilities
using stdio communication protocol, compatible with Claude Desktop.
"""

import json
import sys
import os
from typing import Dict, Any, List
from document_analyzer import DocumentAnalyzer

class MCPServer:
    """
    MCP Server using stdio communication protocol.
    
    This server communicates with Claude Desktop using JSON-RPC over stdio.
    """
    
    def __init__(self):
        self.analyzer = DocumentAnalyzer()
        self.tools = self._define_tools()
        
    def _define_tools(self) -> List[Dict[str, Any]]:
        """Define available MCP tools."""
        return [
            {
                "name": "analyze_document",
                "description": "Perform complete analysis of a document including sentiment, keywords, readability, and statistics",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "document_id": {
                            "type": "string",
                            "description": "ID of the document to analyze"
                        }
                    },
                    "required": ["document_id"]
                }
            },
            {
                "name": "get_sentiment",
                "description": "Analyze sentiment of any text (positive/negative/neutral)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text to analyze for sentiment"
                        }
                    },
                    "required": ["text"]
                }
            },
            {
                "name": "extract_keywords",
                "description": "Extract top keywords from text",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text to extract keywords from"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of keywords to return",
                            "default": 10
                        }
                    },
                    "required": ["text"]
                }
            },
            {
                "name": "add_document",
                "description": "Add a new document to the collection",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "document_data": {
                            "type": "object",
                            "description": "Document data including content, title, author, and category",
                            "properties": {
                                "content": {"type": "string", "description": "Document content"},
                                "title": {"type": "string", "description": "Document title"},
                                "author": {"type": "string", "description": "Document author"},
                                "category": {"type": "string", "description": "Document category"}
                            },
                            "required": ["content", "title"]
                        }
                    },
                    "required": ["document_data"]
                }
            },
            {
                "name": "search_documents",
                "description": "Search documents by content or metadata",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query"
                        }
                    },
                    "required": ["query"]
                }
            }
        ]
    
    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP request."""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "initialize":
                return self._handle_initialize(request_id, params)
            elif method == "tools/list":
                return self._handle_tools_list(request_id)
            elif method == "tools/call":
                return self._handle_tool_call(request_id, params)
            else:
                return self._error_response(request_id, -32601, f"Method not found: {method}")
        
        except Exception as e:
            return self._error_response(request_id, -32603, f"Internal error: {str(e)}")
    
    def _handle_initialize(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize request."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "document-analyzer",
                    "version": "1.0.0"
                }
            }
        }
    
    def _handle_tools_list(self, request_id: Any) -> Dict[str, Any]:
        """Handle tools/list request."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": self.tools
            }
        }
    
    def _handle_tool_call(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request."""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        try:
            if tool_name == "analyze_document":
                result = self._analyze_document(arguments)
            elif tool_name == "get_sentiment":
                result = self._get_sentiment(arguments)
            elif tool_name == "extract_keywords":
                result = self._extract_keywords(arguments)
            elif tool_name == "add_document":
                result = self._add_document(arguments)
            elif tool_name == "search_documents":
                result = self._search_documents(arguments)
            else:
                return self._error_response(request_id, -32602, f"Unknown tool: {tool_name}")
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, indent=2, ensure_ascii=False)
                        }
                    ]
                }
            }
        
        except Exception as e:
            return self._error_response(request_id, -32603, f"Tool execution error: {str(e)}")
    
    def _analyze_document(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a document."""
        document_id = arguments.get("document_id")
        if not document_id:
            raise ValueError("document_id is required")
        
        return self.analyzer.analyze_document(document_id)
    
    def _get_sentiment(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get sentiment of text."""
        text = arguments.get("text")
        if not text:
            raise ValueError("text is required")
        
        return self.analyzer.get_sentiment(text)
    
    def _extract_keywords(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Extract keywords from text."""
        text = arguments.get("text")
        limit = arguments.get("limit", 10)
        
        if not text:
            raise ValueError("text is required")
        
        return self.analyzer.extract_keywords(text, limit)
    
    def _add_document(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new document."""
        document_data = arguments.get("document_data")
        if not document_data:
            raise ValueError("document_data is required")
        
        return self.analyzer.add_document(document_data)
    
    def _search_documents(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Search documents."""
        query = arguments.get("query")
        if not query:
            raise ValueError("query is required")
        
        return self.analyzer.search_documents(query)
    
    def _error_response(self, request_id: Any, code: int, message: str) -> Dict[str, Any]:
        """Create error response."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }
    
    def run(self):
        """Run the MCP server."""
        # Create sample documents if they don't exist
        if not os.path.exists("documents"):
            from server import create_sample_documents
            create_sample_documents()
        
        # Process requests from stdin
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            
            try:
                request = json.loads(line)
                response = self.handle_request(request)
                print(json.dumps(response), flush=True)
            except json.JSONDecodeError:
                error_response = self._error_response(None, -32700, "Parse error")
                print(json.dumps(error_response), flush=True)
            except Exception as e:
                error_response = self._error_response(None, -32603, f"Internal error: {str(e)}")
                print(json.dumps(error_response), flush=True)

def main():
    """Main entry point."""
    server = MCPServer()
    server.run()

if __name__ == "__main__":
    main() 