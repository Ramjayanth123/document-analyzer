# 🖥️ Claude Desktop MCP Server Setup Guide

This guide will help you set up and test the Document Analyzer MCP server with Claude Desktop.

## 📋 Prerequisites

1. **Claude Desktop** installed on your system
2. **Python 3.8+** with our virtual environment set up
3. **Document Analyzer Server** (this project)

## 🔧 Step-by-Step Setup

### Step 1: Locate Claude Desktop Configuration

First, you need to find where Claude Desktop stores its configuration:

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

### Step 2: Create or Edit Configuration File

1. **Navigate to the configuration directory**
2. **Create or edit** `claude_desktop_config.json`
3. **Add the following configuration:**

```json
{
  "mcpServers": {
    "document-analyzer": {
      "command": "python",
      "args": ["E:/Misogi/document-analyzer/mcp_server.py"],
      "env": {
        "PYTHONPATH": "E:/Misogi/document-analyzer"
      }
    }
  }
}
```

**⚠️ Important:** Replace `E:/Misogi/document-analyzer/` with your actual project path!

### Step 3: Verify Python Environment

Make sure your Python environment can access the required packages:

```bash
# Navigate to your project directory
cd E:\Misogi\document-analyzer

# Activate virtual environment
venv\Scripts\activate

# Verify packages are installed
python -c "import textblob, nltk; print('Dependencies OK')"
```

### Step 4: Test MCP Server Standalone

Before connecting to Claude Desktop, test the server directly:

```bash
# In your project directory with venv activated
python mcp_server.py
```

The server should start and wait for JSON-RPC input. You can test with:

```json
{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0.0"}}}
```

### Step 5: Restart Claude Desktop

1. **Close Claude Desktop completely**
2. **Restart Claude Desktop**
3. **Check for MCP server connection**

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
Add a new document with title "My Test Document", author "Test User", category "Testing", and content "This is a test document for the MCP server."
```

## 🔍 Troubleshooting

### Common Issues:

1. **MCP Server Not Found**
   - Check that the path in `claude_desktop_config.json` is correct
   - Ensure Python is in your system PATH
   - Verify the virtual environment has required packages

2. **Permission Errors**
   - Make sure the Python script has execute permissions
   - Check that Claude Desktop can access the file path

3. **Python Import Errors**
   - Activate your virtual environment
   - Install missing packages: `pip install textblob nltk`
   - Check PYTHONPATH in configuration

4. **JSON-RPC Errors**
   - Check server logs for specific error messages
   - Verify the MCP protocol version compatibility

### Debug Steps:

1. **Check Claude Desktop Logs**
   - Look for MCP server connection messages
   - Check for any error messages

2. **Test Server Manually**
   ```bash
   python mcp_server.py
   ```
   
3. **Verify Configuration**
   - Double-check paths in `claude_desktop_config.json`
   - Ensure JSON syntax is valid

## 📊 Expected Results

When working correctly, you should see:

1. **Available Tools** in Claude Desktop interface
2. **Successful tool calls** with proper responses
3. **Document analysis results** with sentiment, keywords, and statistics
4. **Search functionality** working across the document collection

## 🎯 Success Indicators

✅ Claude Desktop shows MCP tools are available  
✅ Document analysis returns complete results  
✅ Sentiment analysis works with custom text  
✅ Keyword extraction produces relevant terms  
✅ Document search finds relevant documents  
✅ New documents can be added to the collection  

## 📞 Need Help?

If you encounter issues:

1. Check the troubleshooting section above
2. Verify all paths and configurations
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