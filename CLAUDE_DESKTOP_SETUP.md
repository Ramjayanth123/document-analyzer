# 🖥️ Claude Desktop MCP Server Setup Guide

This guide will help you set up and test the Document Analyzer MCP server with Claude Desktop using the **official MCP SDK**.

## 📋 Prerequisites

1. **Claude Desktop** installed on your system
2. **Python 3.8+** with our virtual environment set up
3. **Document Analyzer Server** (this project)
4. **Official MCP SDK** (now included in requirements)

## 🔧 Step-by-Step Setup

### Step 1: Install MCP SDK

First, install the official MCP SDK:

```bash
# Navigate to your project directory
cd E:\Misogi\document-analyzer

# Activate virtual environment
venv\Scripts\activate

# Install the MCP SDK
pip install mcp

# Verify installation
python -c "import mcp; print('✓ MCP SDK installed successfully')"
```

### Step 2: Locate Claude Desktop Configuration

Find where Claude Desktop stores its configuration:

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

### Step 3: Create or Edit Configuration File

1. **Navigate to the configuration directory**
2. **Create or edit** `claude_desktop_config.json`
3. **Add the following configuration:**

```json
{
  "mcpServers": {
    "document-analyzer": {
      "command": "python",
      "args": ["E:/Misogi/document-analyzer/mcp_server_official.py"],
      "env": {
        "PYTHONPATH": "E:/Misogi/document-analyzer"
      }
    }
  }
}
```

**⚠️ Important:** Replace `E:/Misogi/document-analyzer/` with your actual project path!

### Step 4: Test MCP Server with Official SDK

Test the server using the official MCP SDK:

```bash
# In your project directory with venv activated
python mcp_server_official.py
```

The server should start and show it's using the official MCP SDK with `@app.tool()` decorators.

### Step 5: Restart Claude Desktop

1. **Close Claude Desktop completely**
2. **Restart Claude Desktop**
3. **Check for MCP server connection**

## 🎯 **Key Features of Official MCP Server**

### **@app.tool() Decorators**
Our server now uses proper MCP decorators:

```python
@app.tool()
async def analyze_document(document_id: str) -> list[TextContent]:
    """Analyze a document with sentiment, keywords, and stats."""
    # Tool implementation
```

### **5 Available Tools:**
1. **`analyze_document`** - Complete document analysis
2. **`get_sentiment`** - Text sentiment analysis
3. **`extract_keywords`** - Keyword extraction
4. **`search_documents`** - Document search
5. **`add_document`** - Add new documents

## 🧪 Testing the MCP Tools

Once Claude Desktop is running with the MCP server connected, you should be able to use these tools:

### 1. Analyze Document
```
Please analyze document doc_001 using the analyze_document tool.
```

### 2. Get Sentiment
```
Can you analyze the sentiment of this text: "I love this amazing product! It works perfectly!"
```

### 3. Extract Keywords
```
Extract the top 5 keywords from this text: "Machine learning and artificial intelligence are transforming technology through automation and data analysis."
```

### 4. Search Documents
```
Search for documents related to "artificial intelligence" in the collection.
```

### 5. Add Document
```
Add a new document with title "My Test Document", content "This is a test document for the MCP server.", author "Test User", and category "Testing".
```

## 🔍 Troubleshooting

### Common Issues:

1. **MCP SDK Not Found**
   - Install MCP SDK: `pip install mcp`
   - Verify installation: `python -c "import mcp; print('OK')"`

2. **Server Not Starting**
   - Check that the path in `claude_desktop_config.json` is correct
   - Ensure Python is in your system PATH
   - Verify the virtual environment has required packages

3. **Import Errors**
   - Activate your virtual environment: `venv\Scripts\activate`
   - Install all dependencies: `pip install -r requirements.txt`
   - Check PYTHONPATH in configuration

### Debug Steps:

1. **Test Server Manually**
   ```bash
   cd E:\Misogi\document-analyzer
   venv\Scripts\activate
   python mcp_server_official.py
   ```

2. **Verify MCP SDK Installation**
   ```bash
   python -c "from mcp.server import Server; print('✓ MCP SDK working')"
   ```

3. **Check Configuration**
   - Double-check paths in `claude_desktop_config.json`
   - Ensure JSON syntax is valid
   - Verify file permissions

## 📊 Expected Results

When working correctly, you should see:

1. **Available Tools** in Claude Desktop interface
2. **Successful tool calls** with proper responses
3. **@app.tool() decorators** working seamlessly
4. **Structured JSON responses** from document analysis
5. **All 5 tools** functioning correctly

## 🎯 Success Indicators

✅ Claude Desktop shows MCP tools are available  
✅ `@app.tool()` decorators are working  
✅ Document analysis returns complete results  
✅ Sentiment analysis works with custom text  
✅ Keyword extraction produces relevant terms  
✅ Document search finds relevant documents  
✅ New documents can be added to the collection  

## 📞 Need Help?

If you encounter issues:

1. Check the troubleshooting section above
2. Verify MCP SDK installation
3. Test the server independently first
4. Check Claude Desktop documentation for MCP setup

## 🔗 Alternative: HTTP Server

If you prefer to use the HTTP server version (for testing with other tools):

```bash
python server.py
```

Then test with:
```bash
python test_client.py
```

This provides a web interface at `http://localhost:8000` for testing the same functionality.

## 🚀 What's New

### **Official MCP SDK Benefits:**
- ✅ **Proper `@app.tool()` decorators**
- ✅ **Automatic tool registration**
- ✅ **Better Claude Desktop integration**
- ✅ **Improved error handling**
- ✅ **Async/await support**
- ✅ **Type validation**

Your MCP server now follows official MCP best practices and should work seamlessly with Claude Desktop! 