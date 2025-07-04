# 🚀 MCP Document Analyzer Server

## 📋 Project Overview

This project implements a **Model Context Protocol (MCP) server** that provides text document analysis capabilities. The server can analyze documents for sentiment, extract keywords, calculate readability scores, and provide basic text statistics. 📊✨

**🎯 Multiple Server Implementations:**
- 🌐 **HTTP Server** (`server.py`) - Web-based testing and development
- 🤖 **Official MCP Server** (`mcp_server_official.py`) - **Claude Desktop integration with @app.tool() decorators**
- 🔧 **Custom MCP Server** (`mcp_server.py`) - Manual JSON-RPC implementation

## 🤖 What is MCP (Model Context Protocol)?

MCP is a protocol that allows AI assistants to interact with external tools and data sources in a standardized way. Think of it as a bridge 🌉 between AI systems and external services - the AI can call specific "tools" (functions) on the server and get structured responses.

**🔑 Key MCP Concepts:**
- **🛠️ Tools**: Functions that the server exposes (like `analyze_document`, `get_sentiment`)
- **📝 Arguments**: Parameters passed to tools (like `document_id`, `text`)
- **📤 Responses**: Structured JSON responses from tool calls
- **🌐 Protocol**: Stdio or HTTP-based communication using JSON-RPC

## 🆕 **New: Official MCP SDK Integration**

This project now includes an **official MCP server** using the MCP Python SDK with proper `@app.tool()` decorators for seamless Claude Desktop integration! 🎉

### 🔧 **Official MCP Server Features:**

```python
# Modern MCP implementation with decorators
@app.tool()
async def analyze_document(document_id: str) -> list[TextContent]:
    """Complete document analysis with sentiment, keywords, and stats."""

@app.tool()
async def get_sentiment(text: str) -> list[TextContent]:
    """Analyze sentiment of any text (positive/negative/neutral)."""

@app.tool()
async def extract_keywords(text: str, limit: int = 10) -> list[TextContent]:
    """Extract top keywords from text."""

@app.tool()
async def search_documents(query: str) -> list[TextContent]:
    """Search documents by content or metadata."""

@app.tool()
async def add_document(title: str, content: str, author: str = "Unknown", category: str = "General") -> list[TextContent]:
    """Add a new document to the collection."""
```

### ✨ **Benefits of Official MCP SDK:**
- ✅ **Automatic tool registration** with Claude Desktop
- ✅ **Built-in type validation** and parameter checking
- ✅ **Better error handling** and async support
- ✅ **Claude Desktop compatibility** following official MCP standards
- ✅ **Simplified development** with decorators

## 🏗️ Project Architecture

### 🤔 Why This Approach?

I chose this architecture for several reasons:

1. **🎯 Simplicity**: Using basic HTTP server and JSON files keeps the implementation straightforward for a class assignment
2. **📚 Educational Value**: Building from scratch helps understand MCP concepts better than using existing frameworks
3. **🧩 Modularity**: Separating analysis logic from server logic makes the code maintainable
4. **🔧 Extensibility**: Easy to add new analysis features or change storage methods
5. **🤖 MCP Compatibility**: Multiple server implementations for different use cases

### 📁 File Structure

```
document-analyzer/
├── 🖥️ server.py                    # HTTP MCP server (web testing)
├── 🤖 mcp_server_official.py       # Official MCP SDK server (Claude Desktop)
├── 🔧 mcp_server.py                # Custom JSON-RPC MCP server
├── 🔬 document_analyzer.py         # Core analysis logic (sentiment, keywords, etc.)
├── 🧪 test_client.py               # Test client for HTTP server
├── 📦 requirements.txt             # Python dependencies (includes MCP SDK)
├── 📋 claude_desktop_config.json   # Claude Desktop configuration
├── 📖 README.md                   # This documentation
├── 🔧 CLAUDE_DESKTOP_SETUP.md     # Claude Desktop setup guide
├── 📝 QUICKSTART.md               # 5-minute setup guide
└── 📂 documents/                  # Created automatically when server runs
    ├── 📄 documents.json          # Document metadata storage
    └── 📁 content/                # Individual document text files
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

### 🎯 **Quick Start Options**

Choose your preferred setup method:

#### 🤖 **Option 1: Claude Desktop Integration (Recommended)**

For seamless Claude Desktop integration with `@app.tool()` decorators:

```bash
# 1. Setup environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 2. Install dependencies (including MCP SDK)
pip install -r requirements.txt

# 3. Test official MCP server
python mcp_server_official.py

# 4. Configure Claude Desktop
# See CLAUDE_DESKTOP_SETUP.md for detailed instructions
```

#### 🌐 **Option 2: HTTP Server (Web Testing)**

For web-based testing and development:

```bash
# 1. Setup environment (same as above)
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start HTTP server
python server.py

# 4. Test with client
python test_client.py
```

#### ⚡ **Option 3: Automated Setup**

Use the automated setup script:

```bash
python setup.py
```

This will:
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Download NLTK data
- ✅ Test the installation

### 🔧 **Manual Setup Details**

#### 1. ⚙️ Setup Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies (including official MCP SDK)
pip install -r requirements.txt
```

#### 2. 🖥️ Start a Server

**🤖 For Claude Desktop (Official MCP):**
```bash
python mcp_server_official.py
```

**🌐 For HTTP Testing:**
```bash
python server.py
```

The servers will:
- 📚 Create sample documents automatically
- 🛠️ Expose 5 MCP tools for document analysis
- 📋 Display available tools and usage information

#### 3. 🧪 Test the Server

**🌐 For HTTP Server:**
```bash
# In another terminal
python test_client.py
```

**🤖 For Claude Desktop:**
- Follow the setup guide in `CLAUDE_DESKTOP_SETUP.md`
- Ask Claude: "What tools do you have available?"
- Use tools like: "Please analyze document doc_001"

### 4. 🔧 Manual Testing

**🌐 HTTP Server Testing:**
```bash
# Health check
curl http://localhost:8000/health

# Get available tools
curl http://localhost:8000/tools

# Analyze sentiment
curl -X POST http://localhost:8000 \
  -H "Content-Type: application/json" \
  -d '{"tool": "get_sentiment", "arguments": {"text": "I love this project!"}}'
```

**🤖 Claude Desktop Testing:**
```
# Example prompts to try:
- "What tools do you have available?"
- "Please analyze document doc_001 using the analyze_document tool"
- "Can you extract keywords from this text: 'Machine learning is transforming AI'"
- "Search for documents about artificial intelligence"
```

## 🔗 MCP Protocol Details

### 📤 **HTTP Server Request Format**
```json
{
  "tool": "tool_name",
  "arguments": {
    "parameter1": "value1",
    "parameter2": "value2"
  }
}
```

### 📥 **HTTP Server Response Format**
```json
{
  "tool": "tool_name",
  "result": {
    // Tool-specific results
  },
  "timestamp": "2024-01-01T12:00:00"
}
```

### 🤖 **Official MCP Server (Claude Desktop)**
The official MCP server uses JSON-RPC over stdio and is automatically handled by Claude Desktop. Tools are called using natural language:

```
"Please use the analyze_document tool to analyze doc_001"
```

Claude Desktop handles the JSON-RPC communication automatically.

### ❌ Error Format
```json
{
  "error": "Error description"
}
```

## 🛠️ **Available MCP Tools**

All server implementations provide these 5 tools:

| Tool | Description | Parameters |
|------|-------------|------------|
| 🔬 `analyze_document` | Complete document analysis | `document_id: str` |
| 😊 `get_sentiment` | Sentiment analysis | `text: str` |
| 🔍 `extract_keywords` | Keyword extraction | `text: str, limit: int = 10` |
| 🔎 `search_documents` | Document search | `query: str` |
| ➕ `add_document` | Add new document | `title: str, content: str, author?: str, category?: str` |

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

### 🤖 MCP Enhancements
- Additional MCP capabilities (resources, prompts)
- Real-time notifications
- Batch processing tools
- Advanced Claude Desktop integrations

### 🔌 Integration Options
- Connect to external APIs (OpenAI, Google Cloud NLP)
- Support for different document formats (PDF, Word, HTML)
- Integration with document management systems
- Real-time collaboration features

## 🎓 Learning Outcomes

By implementing this project, you learn:

1. **🤖 MCP Protocol**: How AI assistants communicate with external tools
2. **🛠️ Official MCP SDK**: Using `@app.tool()` decorators and modern MCP patterns
3. **🌐 HTTP Servers**: Building web services from scratch
4. **📊 Text Analysis**: Fundamental NLP techniques and their applications
5. **🔗 API Design**: Creating clean, consistent interfaces
6. **🚨 Error Handling**: Robust error management in distributed systems
7. **🧪 Testing**: Comprehensive testing strategies for web services
8. **📖 Documentation**: Writing clear technical documentation
9. **🤖 Claude Desktop Integration**: Connecting AI assistants to custom tools

## 🔧 Troubleshooting

### ⚠️ Common Issues

**🤖 Claude Desktop Issues:**
- Server not found: Check `claude_desktop_config.json` path
- MCP SDK import errors: Run `pip install mcp`
- Tools not appearing: Restart Claude Desktop completely

**🌐 HTTP Server Issues:**
- Server won't start: Check if port 8000 is already in use
- Ensure all dependencies are installed
- Verify Python version (3.8+ recommended)

**📊 Analysis errors:**
- TextBlob might need NLTK data: `python -c "import nltk; nltk.download('punkt')"`
- Check document encoding (should be UTF-8)

**🧪 Test client failures:**
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

## 📚 Documentation

- 📖 **README.md** - Complete project documentation (this file)
- 🔧 **CLAUDE_DESKTOP_SETUP.md** - Step-by-step Claude Desktop setup guide
- 📝 **QUICKSTART.md** - 5-minute quick start guide
- 🤖 **Official MCP SDK Documentation** - https://modelcontextprotocol.io/

## 🎯 Conclusion

This MCP Document Analyzer Server demonstrates how to build a functional text analysis service that follows the Model Context Protocol using both traditional HTTP and the modern official MCP SDK approach. The implementation prioritizes simplicity and educational value while providing multiple integration options for different use cases. ✨

The project showcases key concepts in web services, text processing, API design, and modern AI assistant integration, making it an excellent learning tool for understanding how AI assistants interact with external services through the MCP protocol. 🚀

**🌟 Key Highlights:**
- ✅ **3 server implementations** for different use cases
- ✅ **Official MCP SDK integration** with `@app.tool()` decorators
- ✅ **Claude Desktop compatibility** out of the box
- ✅ **16 sample documents** for testing and demonstration
- ✅ **Comprehensive documentation** and setup guides
- ✅ **Educational focus** with clear explanations

---

**�� Happy Coding! 🎉** 