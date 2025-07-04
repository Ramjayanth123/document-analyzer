# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Option 1: Automated Setup (Recommended)
```bash
# Run the setup script
python setup.py

# Follow the instructions to activate environment and start server
```

### Option 2: Manual Setup
```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the server
python server.py
```

### Testing
```bash
# In another terminal (with same virtual environment activated)
python test_client.py
```

## 📋 What You'll See

### Server Output
```
MCP Document Analyzer Server
Running on: http://localhost:8000
Health check: http://localhost:8000/health
Available tools: http://localhost:8000/tools
Press Ctrl+C to stop
```

### Test Client Output
```
✓ Server is running and healthy
✓ Found 5 available tools

TESTING SENTIMENT ANALYSIS
==================================================
Test 1: I love this amazing product! It's fantastic...
Sentiment: positive
Polarity: 0.625
Subjectivity: 0.9

[... more test results ...]

ALL TESTS COMPLETED SUCCESSFULLY!
```

## 🔧 Available MCP Tools

| Tool | Description | Example |
|------|-------------|---------|
| `analyze_document` | Complete document analysis | `{"tool": "analyze_document", "arguments": {"document_id": "doc_001"}}` |
| `get_sentiment` | Sentiment analysis | `{"tool": "get_sentiment", "arguments": {"text": "I love this!"}}` |
| `extract_keywords` | Keyword extraction | `{"tool": "extract_keywords", "arguments": {"text": "AI and machine learning", "limit": 5}}` |
| `add_document` | Add new document | `{"tool": "add_document", "arguments": {"document_data": {...}}}` |
| `search_documents` | Search documents | `{"tool": "search_documents", "arguments": {"query": "artificial intelligence"}}` |

## 🌐 Manual Testing with curl

```bash
# Health check
curl http://localhost:8000/health

# Get sentiment
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d '{"tool": "get_sentiment", "arguments": {"text": "This is amazing!"}}'

# Search documents
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d '{"tool": "search_documents", "arguments": {"query": "technology"}}'
```

## 📁 Project Structure
```
document-analyzer/
├── server.py              # Main MCP server
├── document_analyzer.py   # Analysis logic
├── test_client.py         # Test client
├── setup.py              # Setup script
├── requirements.txt      # Dependencies
├── README.md            # Full documentation
├── QUICKSTART.md        # This file
└── documents/           # Auto-created
    ├── documents.json   # Document metadata
    └── content/         # Document files
```

## 🎯 Next Steps

1. **Read the full documentation**: `README.md`
2. **Explore the sample documents**: Check `documents/` folder after running server
3. **Try different queries**: Test various search terms and text analysis
4. **Add your own documents**: Use the `add_document` tool
5. **Extend the functionality**: Add new analysis features

## 🐛 Troubleshooting

- **Port 8000 in use**: Change PORT in `server.py` line 380
- **Import errors**: Make sure virtual environment is activated
- **NLTK data missing**: Run `python -c "import nltk; nltk.download('punkt')"`
- **Server not responding**: Check firewall settings for localhost

## 💡 Understanding MCP

This project demonstrates the **Model Context Protocol (MCP)**:
- AI assistants can call your server's "tools" (functions)
- Each tool has specific parameters and returns structured data
- The protocol uses simple HTTP + JSON communication
- Perfect for extending AI capabilities with custom services

Ready to explore? Start with `python server.py` and `python test_client.py`! 