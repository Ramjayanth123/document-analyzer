#!/usr/bin/env python3
"""
Test Client for MCP Document Analyzer Server

This script demonstrates how to interact with the MCP Document Analyzer Server
by making HTTP requests to test all available tools.
"""

import json
import requests
import time

class MCPTestClient:
    """Test client for the MCP Document Analyzer Server."""
    
    def __init__(self, base_url="http://localhost:8000"):
        """Initialize the test client."""
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self):
        """Check if the server is running."""
        try:
            response = self.session.get(f"{self.base_url}/health")
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def get_available_tools(self):
        """Get list of available MCP tools."""
        try:
            response = self.session.get(f"{self.base_url}/tools")
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error getting tools: {e}")
            return None
    
    def call_tool(self, tool_name, arguments):
        """Call an MCP tool with given arguments."""
        try:
            payload = {
                "tool": tool_name,
                "arguments": arguments
            }
            
            response = self.session.post(
                self.base_url,
                json=payload,
                headers={'Content-Type': 'application/json'}
            )
            
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {e}"}
    
    def test_sentiment_analysis(self):
        """Test sentiment analysis functionality."""
        print("\n" + "="*60)
        print("TESTING SENTIMENT ANALYSIS")
        print("="*60)
        
        test_texts = [
            "I love this amazing product! It's fantastic and works perfectly!",
            "This is terrible. I hate it and it doesn't work at all.",
            "The weather is okay today. Nothing special to report.",
            "Machine learning is transforming various industries through automation."
        ]
        
        for i, text in enumerate(test_texts, 1):
            print(f"\nTest {i}: {text[:50]}...")
            result = self.call_tool("get_sentiment", {"text": text})
            
            if "error" in result:
                print(f"Error: {result['error']}")
            else:
                sentiment_data = result.get("result", {})
                print(f"Sentiment: {sentiment_data.get('sentiment', 'N/A')}")
                print(f"Polarity: {sentiment_data.get('polarity', 'N/A')}")
                print(f"Subjectivity: {sentiment_data.get('subjectivity', 'N/A')}")
    
    def test_keyword_extraction(self):
        """Test keyword extraction functionality."""
        print("\n" + "="*60)
        print("TESTING KEYWORD EXTRACTION")
        print("="*60)
        
        test_text = """
        Artificial intelligence and machine learning are revolutionizing technology.
        Deep learning algorithms enable natural language processing and computer vision.
        Neural networks process data to recognize patterns and make predictions.
        AI applications include autonomous vehicles, recommendation systems, and medical diagnosis.
        """
        
        print(f"Text: {test_text[:100]}...")
        result = self.call_tool("extract_keywords", {"text": test_text, "limit": 8})
        
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            keywords = result.get("result", {}).get("keywords", [])
            print(f"\nTop {len(keywords)} Keywords:")
            for i, kw in enumerate(keywords, 1):
                print(f"{i}. {kw['keyword']} (frequency: {kw['frequency']})")
    
    def test_document_search(self):
        """Test document search functionality."""
        print("\n" + "="*60)
        print("TESTING DOCUMENT SEARCH")
        print("="*60)
        
        search_queries = [
            "artificial intelligence",
            "climate change",
            "technology",
            "environment"
        ]
        
        for query in search_queries:
            print(f"\nSearching for: '{query}'")
            result = self.call_tool("search_documents", {"query": query})
            
            if "error" in result:
                print(f"Error: {result['error']}")
            else:
                results = result.get("result", {}).get("results", [])
                print(f"Found {len(results)} documents:")
                for doc in results[:3]:  # Show top 3 results
                    print(f"  - {doc.get('title', 'N/A')} (Score: {doc.get('relevance_score', 0)})")
    
    def test_document_analysis(self):
        """Test complete document analysis."""
        print("\n" + "="*60)
        print("TESTING DOCUMENT ANALYSIS")
        print("="*60)
        
        # First, search for a document to analyze
        search_result = self.call_tool("search_documents", {"query": "artificial intelligence"})
        
        if "error" in search_result:
            print(f"Error searching documents: {search_result['error']}")
            return
        
        results = search_result.get("result", {}).get("results", [])
        if not results:
            print("No documents found to analyze")
            return
        
        # Analyze the first document found
        doc_id = results[0]["document_id"]
        print(f"Analyzing document: {doc_id}")
        
        result = self.call_tool("analyze_document", {"document_id": doc_id})
        
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            analysis = result.get("result", {})
            
            print(f"\nDocument: {analysis.get('metadata', {}).get('title', 'N/A')}")
            print(f"Author: {analysis.get('metadata', {}).get('author', 'N/A')}")
            print(f"Category: {analysis.get('metadata', {}).get('category', 'N/A')}")
            
            # Sentiment
            sentiment = analysis.get("sentiment", {})
            print(f"\nSentiment: {sentiment.get('sentiment', 'N/A')}")
            print(f"Polarity: {sentiment.get('polarity', 'N/A')}")
            
            # Keywords
            keywords = analysis.get("keywords", [])[:5]  # Top 5
            print(f"\nTop Keywords:")
            for kw in keywords:
                print(f"  - {kw.get('keyword', 'N/A')} ({kw.get('frequency', 0)})")
            
            # Readability
            readability = analysis.get("readability", {})
            print(f"\nReadability:")
            print(f"  - Reading Level: {readability.get('reading_level', 'N/A')}")
            print(f"  - Flesch Score: {readability.get('flesch_score', 'N/A')}")
            
            # Statistics
            stats = analysis.get("statistics", {})
            print(f"\nStatistics:")
            print(f"  - Word Count: {stats.get('word_count', 'N/A')}")
            print(f"  - Sentence Count: {stats.get('sentence_count', 'N/A')}")
            print(f"  - Avg Words/Sentence: {stats.get('avg_words_per_sentence', 'N/A')}")
    
    def test_add_document(self):
        """Test adding a new document."""
        print("\n" + "="*60)
        print("TESTING ADD DOCUMENT")
        print("="*60)
        
        new_doc = {
            "title": "Test Document from Client",
            "author": "Test Client",
            "category": "Testing",
            "content": """
            This is a test document created by the test client to demonstrate
            the add_document functionality of the MCP Document Analyzer Server.
            
            This document contains multiple sentences to test various analysis
            features. The content is designed to be moderately positive in
            sentiment and contains keywords related to testing and demonstration.
            
            The document serves as an example of how new content can be added
            to the document collection and subsequently analyzed using the
            various tools provided by the server.
            """
        }
        
        result = self.call_tool("add_document", {"document_data": new_doc})
        
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            doc_result = result.get("result", {})
            doc_id = doc_result.get("document_id", "N/A")
            print(f"Successfully added document: {doc_id}")
            print(f"Message: {doc_result.get('message', 'N/A')}")
            
            # Now analyze the newly added document
            print(f"\nAnalyzing newly added document...")
            analysis_result = self.call_tool("analyze_document", {"document_id": doc_id})
            
            if "error" in analysis_result:
                print(f"Error analyzing new document: {analysis_result['error']}")
            else:
                analysis = analysis_result.get("result", {})
                sentiment = analysis.get("sentiment", {})
                keywords = analysis.get("keywords", [])[:3]
                
                print(f"Sentiment: {sentiment.get('sentiment', 'N/A')}")
                print(f"Top Keywords: {', '.join([kw.get('keyword', '') for kw in keywords])}")
    
    def run_all_tests(self):
        """Run all test functions."""
        print("MCP Document Analyzer Server - Test Client")
        print("="*60)
        
        # Check if server is running
        if not self.health_check():
            print("ERROR: Server is not running!")
            print("Please start the server first by running: python server.py")
            return
        
        print("✓ Server is running and healthy")
        
        # Get available tools
        tools = self.get_available_tools()
        if tools:
            print(f"✓ Found {len(tools.get('tools', []))} available tools")
        else:
            print("✗ Could not retrieve available tools")
        
        # Run individual tests
        try:
            self.test_sentiment_analysis()
            self.test_keyword_extraction()
            self.test_document_search()
            self.test_document_analysis()
            self.test_add_document()
            
            print("\n" + "="*60)
            print("ALL TESTS COMPLETED SUCCESSFULLY!")
            print("="*60)
            
        except Exception as e:
            print(f"\nTest failed with error: {e}")
            print("="*60)

def main():
    """Main function to run the test client."""
    client = MCPTestClient()
    client.run_all_tests()

if __name__ == "__main__":
    main() 