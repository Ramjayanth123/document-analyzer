# 🚀 MCP Document Analyzer Server

## 📋 Project Overview

This project implements a **Model Context Protocol (MCP) server** that provides text document analysis capabilities. The server can analyze documents for sentiment, extract keywords, calculate readability scores, and provide basic text statistics. 📊✨

## 🤖 What is MCP (Model Context Protocol)?

MCP is a protocol that allows AI assistants to interact with external tools and data sources in a standardized way. Think of it as a bridge 🌉 between AI systems and external services - the AI can call specific "tools" (functions) on the server and get structured responses.

**🔑 Key MCP Concepts:**
- **🛠️ Tools**: Functions that the server exposes (like `analyze_document`, `get_sentiment`)
- **📝 Arguments**: Parameters passed to tools (like `document_id`, `text`)
- **📤 Responses**: Structured JSON responses from tool calls
- **🌐 Protocol**: HTTP-based communication using JSON

## 🏗️ Project Architecture

### 🤔 Why This Approach?

I chose this architecture for several reasons:

1. **🎯 Simplicity**: Using basic HTTP server and JSON files keeps the implementation straightforward for a class assignment
2. **📚 Educational Value**: Building from scratch helps understand MCP concepts better than using existing frameworks
3. **🧩 Modularity**: Separating analysis logic from server logic makes the code maintainable
4. **🔧 Extensibility**: Easy to add new analysis features or change storage methods

### 📁 File Structure

```
document-analyzer/
├── 🖥️ server.py              # Main MCP server (HTTP request handling)
├── 🔬 document_analyzer.py   # Core analysis logic (sentiment, keywords, etc.)
├── 🧪 test_client.py         # Test client to demonstrate functionality
├── 📦 requirements.txt       # Python dependencies
├── 📖 README.md             # This documentation
└── 📂 documents/            # Created automatically when server runs
    ├── 📄 documents.json    # Document metadata storage
    └── 📁 content/          # Individual document text files
        ├── 📝 doc_001.txt
        ├── 📝 doc_002.txt
        └── ...
```

## 🔧 Implementation Details

### 1. 💾 Document Storage (`documents/`)

**🤔 Why JSON Files?**
- ✅ Simple to implement and understand
- 🐛 Human-readable for debugging
- 🚫 No database setup required
- 📊 Sufficient for assignment scope (15+ documents)

**🏗️ Structure:**
- `documents.json`: Stores metadata (title, author, category, filename)
- `content/`: Individual `.txt` files with document content
- This separation keeps metadata queries fast while allowing full-text search

### 2. 🔬 Core Analysis Module (`document_analyzer.py`)

This module contains all the text analysis logic:

#### 😊 Sentiment Analysis
- **📚 Library**: TextBlob (simple and effective)
- **📊 Method**: Polarity scoring (-1 to +1)
- **🏷️ Categories**: Positive (>0.1), Negative (<-0.1), Neutral (between)
- **✨ Why TextBlob**: Easy to use, no complex setup, good for educational purposes

#### 🔍 Keyword Extraction
- **⚙️ Method**: Word frequency counting with stop word filtering
- **🎯 Approach**: Simple but effective for most texts
- **🚫 Stop Words**: Common words (the, and, is, etc.) filtered out
- **💡 Why This Approach**: Transparent, explainable, no complex NLP models needed

#### 📖 Readability Scoring
- **📐 Formula**: Simplified Flesch Reading Ease
- **🧮 Calculation**: Based on average sentence length and syllable count
- **📊 Levels**: Very easy to very difficult (7 categories)
- **🏆 Why Flesch**: Well-established, widely understood metric

#### 📈 Basic Statistics
- 🔤 Character count (with/without spaces)
- 📝 Word count, sentence count, paragraph count
- 📏 Average words per sentence
- **🎯 Why These Metrics**: Fundamental text properties useful for analysis

### 3. 🖥️ MCP Server (`server.py`)

The HTTP server that implements the MCP protocol:

#### 🏗️ Server Design
- **🔧 Base**: Python's built-in `http.server` (no external dependencies)
- **🌐 Protocol**: HTTP with JSON payloads
- **🔗 Endpoints**: 
  - `GET /health` - Health check ❤️
  - `GET /tools` - List available tools 🛠️
  - `POST /` - Tool execution ⚡

#### 🛠️ MCP Tool Implementation
Each tool follows this pattern:
1. ✅ Validate required arguments
2. 🔄 Call appropriate analyzer method
3. 📤 Return structured JSON response
4. 🚨 Handle errors gracefully

**🎯 Available Tools:**
- `analyze_document(document_id)` - Complete document analysis 📊
- `get_sentiment(text)` - Sentiment analysis for any text 😊
- `extract_keywords(text, limit)` - Keyword extraction 🔍
- `add_document(document_data)` - Add new document ➕
- `search_documents(query)` - Search by content/metadata 🔎

### 4. 🧪 Test Client (`test_client.py`)

Demonstrates how to interact with the MCP server:
- 📡 Makes HTTP requests to test all tools
- 📋 Shows expected request/response formats
- ✅ Validates server functionality
- 📖 Serves as usage example

## 🤔 Technical Decisions Explained

### 🐍 Why Python?
- 🛠️ Rich ecosystem for text processing (TextBlob, NLTK, regex)
- 🖥️ Simple HTTP server capabilities
- 📚 Easy to understand and modify
- ⚡ Good for rapid prototyping

### 🌐 Why HTTP Instead of WebSockets?
- 🎯 Simpler to implement and test
- 🔧 Standard HTTP tools work (curl, Postman, browsers)
- 🐛 Stateless design is easier to debug
- ✅ Sufficient for the assignment requirements

### 🧮 Why Simple Algorithms?
- **🔍 Transparency**: Easy to understand how results are calculated
- **⚡ Speed**: Fast processing without complex model loading
- **🔒 Reliability**: Fewer dependencies, less likely to break
- **📚 Educational**: Shows fundamental concepts without black-box complexity

### 📄 Why JSON Storage?
- **👁️ Human-readable**: Easy to inspect and debug
- **🎯 Simple**: No database setup or SQL knowledge required
- **📦 Portable**: Works across different systems
- **✅ Sufficient**: Handles 15+ documents easily

## 📚 Sample Documents

The server automatically creates 15+ sample documents covering various topics:
- 💻 Technology (AI, quantum computing, space exploration)
- 🌍 Environment (climate change, renewable energy)
- 🏥 Health (sleep science, psychology)
- 🎨 Culture (music, storytelling, urban gardening)
- 💰 Economics (future of work, cryptocurrency)
- 🧘 Philosophy (mindfulness, ethics)

**🎯 Why This Variety?**
- 📝 Tests analysis across different writing styles
- 😊 Demonstrates sentiment analysis on various topics
- 🔍 Provides diverse keyword extraction examples
- 📖 Shows readability differences between technical and casual writing

## 🚀 Installation and Usage

### 1. ⚙️ Setup Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. 🖥️ Start the Server
```bash
python server.py
```

The server will:
- 📚 Create sample documents automatically
- 🌐 Start listening on `http://localhost:8000`
- 📋 Display available tools and usage information

### 3. 🧪 Test the Server
```bash
# In another terminal
python test_client.py
```

This will run comprehensive tests of all MCP tools.

### 4. 🔧 Manual Testing
You can also test manually using curl:

```bash
# Health check
curl http://localhost:8000/health

# Get available tools
curl http://localhost:8000/tools

# Analyze sentiment
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d '{"tool": "get_sentiment", "arguments": {"text": "I love this project!"}}'

# Search documents
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d '{"tool": "search_documents", "arguments": {"query": "artificial intelligence"}}'
```

## 🔗 MCP Protocol Details

### 📤 Request Format
```json
{
  "tool": "tool_name",
  "arguments": {
    "parameter1": "value1",
    "parameter2": "value2"
  }
}
```

### 📥 Response Format
```json
{
  "tool": "tool_name",
  "result": {
    // Tool-specific results
  },
  "timestamp": "2024-01-01T12:00:00"
}
```

### ❌ Error Format
```json
{
  "error": "Error description"
}
```

## 🔮 Extension Possibilities

This implementation can be extended in several ways:

### 🧠 Analysis Enhancements
- More sophisticated sentiment analysis (VADER, transformers)
- Named Entity Recognition (NER)
- Topic modeling
- Language detection
- Plagiarism detection

### 💾 Storage Improvements
- SQLite database for better querying
- Full-text search with indexing
- Document versioning
- Bulk import/export

### 🖥️ Server Features
- Authentication and authorization
- Rate limiting
- Caching for frequently accessed documents
- WebSocket support for real-time updates
- API documentation generation

### 🔌 Integration Options
- Connect to external APIs (OpenAI, Google Cloud NLP)
- Support for different document formats (PDF, Word, HTML)
- Integration with document management systems
- Real-time collaboration features

## 🎓 Learning Outcomes

By implementing this project, you learn:

1. **🤖 MCP Protocol**: How AI assistants communicate with external tools
2. **🌐 HTTP Servers**: Building web services from scratch
3. **📊 Text Analysis**: Fundamental NLP techniques and their applications
4. **🔗 API Design**: Creating clean, consistent interfaces
5. **🚨 Error Handling**: Robust error management in distributed systems
6. **🧪 Testing**: Comprehensive testing strategies for web services
7. **📖 Documentation**: Writing clear technical documentation

## 🔧 Troubleshooting

### ⚠️ Common Issues

**Server won't start:**
- Check if port 8000 is already in use
- Ensure all dependencies are installed
- Verify Python version (3.7+ recommended)

**Analysis errors:**
- TextBlob might need NLTK data: `python -c "import nltk; nltk.download('punkt')"`
- Check document encoding (should be UTF-8)

**Test client failures:**
- Ensure server is running before starting tests
- Check firewall settings for localhost connections
- Verify requests library is installed

### ⚡ Performance Considerations

For production use, consider:
- Using a proper web framework (FastAPI, Flask)
- Implementing connection pooling
- Adding caching for frequently analyzed documents
- Using a real database for better query performance
- Implementing proper logging and monitoring

## 🎯 Conclusion

This MCP Document Analyzer Server demonstrates how to build a functional text analysis service that follows the Model Context Protocol. The implementation prioritizes simplicity and educational value while providing a solid foundation for more advanced features. ✨

The project showcases key concepts in web services, text processing, and API design, making it an excellent learning tool for understanding how AI assistants interact with external services. 🚀

---

**🎉 Happy Coding! 🎉** 