# 🛠️ Manual Setup for Yango Tech MCP Server

If the automatic installer `python3 install.py` doesn't work, use these instructions for manual setup.

---

## 📋 Preparation (same for all IDEs)

### Step 1: Create virtual environment

```bash
# Go to project folder
cd /path/to/yangotech_mcp

# Create virtual environment
python3 -m venv .venv

# Activate it
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

### Step 2: Install dependencies

```bash
# Update pip
python -m pip install --upgrade pip

# Install dependencies
pip install fastmcp>=2.5.0 httpx>=0.25.0 pydantic>=2.0.0 python-dotenv>=1.0.0
```

### Step 3: Test functionality

```bash
# Set environment variables
export YANGO_TECH_API_KEY="your_api_key_here"
export YANGO_TECH_BASE_URL="https://api.tst.eu.cloudretail.tech"

# Test connection
python test_api_connection.py

# Check MCP server
python server.py
```

---

## 🎯 Setup for Claude Desktop

### Step 1: Find configuration file

**macOS:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```bash
%APPDATA%/Claude/claude_desktop_config.json
```

**Linux:**
```bash
~/.config/Claude/claude_desktop_config.json
```

### Step 2: Open configuration file

```bash
# macOS
open ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Windows
notepad "%APPDATA%\Claude\claude_desktop_config.json"

# Linux
nano ~/.config/Claude/claude_desktop_config.json
```

### Step 3: Add configuration

**If file is empty or new:**
```json
{
  "mcpServers": {
    "yango-tech": {
      "command": "/opt/homebrew/opt/python@3.13/bin/python3.13",
      "args": ["/FULL_PATH/yangotech_mcp/server.py"],
      "cwd": "/FULL_PATH/yangotech_mcp",
      "env": {
        "PYTHONPATH": "/FULL_PATH/yangotech_mcp/.venv/lib/python3.13/site-packages",
        "YANGO_TECH_API_KEY": "your_api_key_here",
        "YANGO_TECH_BASE_URL": "https://api.tst.eu.cloudretail.tech",
        "YANGO_TECH_TIMEOUT": "30",
        "YANGO_TECH_MAX_RETRIES": "3"
      }
    }
  }
}
```

**If file already contains other MCP servers:**
```json
{
  "mcpServers": {
    "existing-server": {
      "command": "...",
      "args": ["..."]
    },
    "yango-tech": {
      "command": "/opt/homebrew/opt/python@3.13/bin/python3.13",
      "args": ["/FULL_PATH/yangotech_mcp/server.py"],
      "cwd": "/FULL_PATH/yangotech_mcp",
      "env": {
        "PYTHONPATH": "/FULL_PATH/yangotech_mcp/.venv/lib/python3.13/site-packages",
        "YANGO_TECH_API_KEY": "your_api_key_here",
        "YANGO_TECH_BASE_URL": "https://api.tst.eu.cloudretail.tech",
        "YANGO_TECH_TIMEOUT": "30",
        "YANGO_TECH_MAX_RETRIES": "3"
      }
    }
  }
}
```

### Step 4: Replace paths and keys

1. **Replace** `/FULL_PATH/yangotech_mcp` with actual path to your project
2. **Replace** `your_api_key_here` with your Yango Tech API key

**For Windows use paths like:**
```json
"command": "C:\\path\\to\\yangotech_mcp\\.venv\\Scripts\\python.exe",
"cwd": "C:\\path\\to\\yangotech_mcp"
```

### Step 5: Restart Claude Desktop

---

## 🖱️ Setup for Cursor IDE

### Step 1: Open Cursor settings

1. Press `Cmd/Ctrl + ,` to open settings
2. In left panel find **"MCP"**
3. Click **"Add new global MCP server"**

### Step 2: Add configuration

**Primary option (recommended):**
```json
{
  "command": "/FULL_PATH/yangotech_mcp/.venv/bin/python",
  "args": ["server.py"],
  "cwd": "/FULL_PATH/yangotech_mcp",
  "env": {
    "YANGO_TECH_API_KEY": "your_api_key_here",
    "YANGO_TECH_BASE_URL": "https://api.tst.eu.cloudretail.tech",
    "YANGO_TECH_TIMEOUT": "30",
    "YANGO_TECH_MAX_RETRIES": "3"
  }
}
```

**Alternative option (if there are path issues):**
```json
{
  "command": "python3",
  "args": ["server.py"],
  "cwd": "/FULL_PATH/yangotech_mcp",
  "env": {
    "PYTHONPATH": "/FULL_PATH/yangotech_mcp",
    "PATH": "/FULL_PATH/yangotech_mcp/.venv/bin:$PATH",
    "YANGO_TECH_API_KEY": "your_api_key_here",
    "YANGO_TECH_BASE_URL": "https://api.tst.eu.cloudretail.tech",
    "YANGO_TECH_TIMEOUT": "30",
    "YANGO_TECH_MAX_RETRIES": "3"
  }
}
```

### Step 3: Specify server name

In **"Server name"** field enter: `yango-tech`

### Step 4: Replace paths and keys

1. **Replace** `/FULL_PATH/yangotech_mcp` with actual path to your project  
2. **Replace** `your_api_key_here` with your Yango Tech API key

### Step 5: Save and restart Cursor

---

## 🔧 Getting full paths

### Get project path:
```bash
cd yangotech_mcp
pwd
# Result: /Users/username/yangotech_mcp
```

### Get Python path in virtual environment:
```bash
# macOS/Linux
which python
# Result: /Users/username/yangotech_mcp/.venv/bin/python

# Windows  
where python
# Result: C:\Users\username\yangotech_mcp\.venv\Scripts\python.exe
```

---

## 🔑 API Key Setup


### Your own key
Get API key from Yango Tech and use it.

---

## 🧪 Testing functionality

After setup you should have **6 Yango Tech tools with product name enrichment:**

1. `get_order_details` - Get order details with product names
2. `get_order_status` - Get order status  
3. `get_all_products` - Get all products with display names
4. `get_products_batch` - Get products with pagination and names
5. `get_all_stocks` - Get all stocks with product names
6. `get_stocks_batch` - Get stocks with pagination and names

**🎯 Key Feature:** All tools show user-friendly product names instead of cryptic product IDs!

### Test commands:

- **"Show 5 products from Yango Tech catalog"** (with product names)
- **"Show product stocks in stores"** (with product names)
- **"Show details of order 240920-728268"** (with enriched cart items)
- **"Get order status for 240920-728268"**

---

## 🔧 Troubleshooting

### Problem: "command not found" or "No such file"
**Solution:** Check correctness of Python and project folder paths

### Problem: "Module not found"
**Solution:** 
```bash
# Activate virtual environment
source .venv/bin/activate
# Reinstall dependencies
pip install fastmcp httpx pydantic python-dotenv
```

### Problem: "Invalid API key"
**Solution:** Check API key correctness or use test key

### Problem: Tools don't appear
**Solution:**
1. Check JSON syntax in configuration
2. Restart IDE
3. Check IDE logs

### Problem: "Permission denied"
**Solution:**
```bash
# Make Python file executable
chmod +x .venv/bin/python
chmod +x server.py
```

---

## 💡 Alternative ways to run

### Via bash script (Unix systems)

Create file `run_server.sh`:
```bash
#!/bin/bash
cd /FULL_PATH/yangotech_mcp
export YANGO_TECH_API_KEY="your_key"
export YANGO_TECH_BASE_URL="https://api.tst.eu.cloudretail.tech"
.venv/bin/python server.py
```

Use in configuration:
```json
{
  "command": "/FULL_PATH/yangotech_mcp/run_server.sh"
}
```

### Via batch file (Windows)

Create file `run_server.bat`:
```batch
@echo off
cd /d C:\path\to\yangotech_mcp
set YANGO_TECH_API_KEY=your_key
set YANGO_TECH_BASE_URL=https://api.tst.eu.cloudretail.tech
.venv\Scripts\python.exe server.py
```

Use in configuration:
```json
{
  "command": "C:\\path\\to\\yangotech_mcp\\run_server.bat"
}
```

---

**🎯 Result: Yango Tech MCP server works in Claude Desktop or Cursor IDE!** 