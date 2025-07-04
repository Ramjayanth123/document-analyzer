#!/usr/bin/env python3
"""
Official MCP Document Analyzer Server using @mcp.tool decorators

This server uses the official MCP Python SDK with proper tool decorators
that Claude Desktop expects.
"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from document_analyzer import DocumentAnalyzer
import json

# Initialize the MCP server
app = Server("document-analyzer")

# Initialize document analyzer
analyzer = DocumentAnalyzer()

@app.tool()
async def analyze_document(document_id: str) -> list[TextContent]:
    """
    Perform complete analysis of a document including sentiment, keywords, readability, and statistics.
    
    Args:
        document_id: ID of the document to analyze
    """
    try:
        result = analyzer.analyze_document(document_id)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error analyzing document: {str(e)}")]

@app.tool()
async def get_sentiment(text: str) -> list[TextContent]:
    """
    Analyze sentiment of any text (positive/negative/neutral).
    
    Args:
        text: Text to analyze for sentiment
    """
    try:
        result = analyzer.get_sentiment(text)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error analyzing sentiment: {str(e)}")]

@app.tool()
async def extract_keywords(text: str, limit: int = 10) -> list[TextContent]:
    """
    Extract top keywords from text.
    
    Args:
        text: Text to extract keywords from
        limit: Maximum number of keywords to return (default: 10)
    """
    try:
        result = analyzer.extract_keywords(text, limit)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error extracting keywords: {str(e)}")]

@app.tool()
async def search_documents(query: str) -> list[TextContent]:
    """
    Search documents by content or metadata.
    
    Args:
        query: Search query
    """
    try:
        result = analyzer.search_documents(query)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error searching documents: {str(e)}")]

@app.tool()
async def add_document(title: str, content: str, author: str = "Unknown", category: str = "General") -> list[TextContent]:
    """
    Add a new document to the collection.
    
    Args:
        title: Document title
        content: Document content
        author: Document author (default: "Unknown")
        category: Document category (default: "General")
    """
    try:
        document_data = {
            "title": title,
            "content": content,
            "author": author,
            "category": category
        }
        result = analyzer.add_document(document_data)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error adding document: {str(e)}")]

async def main():
    """Main entry point for the MCP server."""
    # Create sample documents if they don't exist
    import os
    if not os.path.exists("documents"):
        from server import create_sample_documents
        create_sample_documents()
    
    # Run the server
    async with stdio_server() as streams:
        await app.run(streams[0], streams[1])

if __name__ == "__main__":
    asyncio.run(main()) 