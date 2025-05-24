# 🚀 Yango Tech MCP Server - One Command Installation

## 🛒 Yango Tech Integration

This project provides integration with **[Yango Tech](https://yango-tech.com/)** - a leading platform for ecommerce automation.

**Yango Tech is part of Yango Group**, a global tech company that transforms the everyday business of people around the world:

📊 **150m+** rides since 2018  
💰 **$2.5B+** GMV  
✅ **99.99%** orders delivered without missing items  
📦 **1.3M+** daily orders

**Yango Tech** offers comprehensive solutions for:
- 🌐 **APP Website applications**
- 🏪 **Order management** and logistics
- 📦 **Real-time inventory management** 
- 🛍️ **Product cataloging** with detailed information
- 🚚 **Delivery and order fulfillment**
- 📊 **Analytics and sales reporting**
- 🔄 **API integration** for B2B automation

Through this MCP server, you can easily interact with the Yango Tech API directly from Claude Desktop or Cursor IDE, gaining access to orders, products, stock levels, and other platform information.

## For Users - Simple Installation

**Download this project and run one command:**

```bash
python3 install.py
```

**Done! Everything will be configured automatically.** 🎉

---

## What the installer does:

1. ✅ **Automatically detects your OS** (Mac/Windows/Linux)
2. ✅ **Finds Python** and creates virtual environment
3. ✅ **Installs all dependencies** automatically (including FastMCP 2.5+)
4. ✅ **Detects installed IDEs** (Claude Desktop & Cursor IDE)
5. ✅ **Offers test API key** or your own
6. ✅ **Creates IDE configurations** automatically (if IDEs installed)
7. ✅ **Generates config files** in project root for manual setup
8. ✅ **Tests functionality** with real API
9. ✅ **Shows instructions** for next steps

**💡 Works even without IDEs installed** - configuration files are always generated!

---

# 🎯 **POWERFUL IDE INTEGRATION**

## 🤖 **Claude Desktop & Cursor IDE Ready!**

After installation, you'll have **seamless integration** with:

### 🖥️ **Claude Desktop** 
**Professional AI assistant with Yango Tech powers**
- 💬 **Natural language queries** to Yango Tech API
- 🔍 **Smart product search** with readable names  
- 📋 **Order management** through conversation
- 📊 **Real-time inventory** checking

#### 📸 **See Claude Desktop in Action:**

**🛍️ Product Catalog Analysis:**
![Claude Product Report](source/claude%20product%20report.png)

**🎬 Live Product Search Demo:**

https://github.com/user-attachments/assets/claude-products-report-video.mov

**📦 Inventory Management:**
![Claude Stock Report](source/claude%20stock%20report.png)

**📋 Order Details Lookup:**
![Claude Order Detail](source/claude%20order%20detail.png)

**🔍 Order Status Tracking:**
![Claude Order Status](source/claude%20order%20status.png)

### ⚡ **Cursor IDE**
**AI-powered code editor with business data access**
- 🛠️ **Code while querying** [Yango Tech](https://yango-tech.com/) data
- 🔄 **API integration** directly in your workflow
- 📝 **Documentation generation** with real data
- 🚀 **Rapid prototyping** with live business insights

### 🎨 **Why This Is Game-Changing:**

**Instead of switching between multiple tools**, you can:
- ✨ **Ask Claude**: *"Show me details for order 240920-728268"*
- ✨ **Ask Cursor**: *"What products are low in stock at store L001?"*  
- ✨ **Get instant answers** with **human-readable product names**
- ✨ **Work faster** with **natural language** instead of complex API calls

**🔗 All powered by [Yango Tech](https://yango-tech.com/) - your ecommerce automation platform!**

---

## After installation

1. **Restart Claude Desktop and/or Cursor IDE** (if installed)
2. **You'll have 6 Yango Tech tools with product name enrichment:**
   - `get_order_details` - Get order details with product names
   - `get_order_status` - Get order status  
   - `get_all_products` - Get all products with display names
   - `get_products_batch` - Get products with pagination and names
   - `get_all_stocks` - Get all stocks with product names
   - `get_stocks_batch` - Get stocks with pagination and names

**🎯 Key Feature:** All tools show user-friendly product names instead of cryptic product IDs!

---

## 📁 Generated Configuration Files

The installer always creates these files in the project root:

- **`claude_desktop_config.json`** - Ready-to-use Claude Desktop configuration
- **`cursor_settings.json`** - Ready-to-use Cursor IDE configuration

**Use these files for:**
- Manual IDE setup
- Backup configurations
- Copying settings to other machines
- Troubleshooting

---

## 🧪 Test commands for Claude Desktop & Cursor IDE:

- **"Show 5 products from Yango Tech catalog"** (with product names)
- **"Show product stocks in stores"** (with product names)
- **"Show details of order 240920-728268"** (with enriched cart items)
- **"Get order status for 240920-728268"**

---

## ⚙️ Requirements

- **Python 3.8+** (automatically detected and verified)
- **Internet** for downloading dependencies
- **Claude Desktop** and/or **Cursor IDE** (optional - configs generated anyway)

### 🐍 Don't have Python installed?

**No problem!** If Python is missing or too old, the installer shows detailed installation guides:

- **macOS**: Official installer, Homebrew, or pyenv
- **Windows**: Official installer (⚠️ check "Add to PATH"), Microsoft Store, or Chocolatey  
- **Linux**: Package manager (`apt`, `dnf`, `pacman`) or from source

**Why Python 3.8+?** Required for FastMCP framework compatibility.

**Quick check**: Run `python3 --version` or `python --version`

**📖 Detailed guide**: See [PYTHON_SETUP.md](PYTHON_SETUP.md) for step-by-step instructions

---

## 🧹 Complete Environment Reset

If you need to completely clean and reinstall:

```bash
python3 cleanup.py
python3 install.py
```

The cleanup script removes:
- Virtual environment
- Configuration files from both IDEs
- Generated configuration files
- Environment files
- Cache files

---

## 🌍 API Endpoints

- **Test Environment**: `https://api.tst.eu.cloudretail.tech`
- **Production Environment**: `https://api.retailtech.yango.com`

---

## 🛠️ For Developers

<details>
<summary>Technical Information</summary>

### Project Architecture

```
yangotech_mcp/
├── install.py               # 🎯 Universal installer  
├── cleanup.py               # 🧹 Complete cleanup script
├── server.py                # FastMCP server
├── client.py                # HTTP client for Yango Tech API
├── models.py                # Pydantic data models
├── claude_desktop_config.json  # Generated Claude config
├── cursor_settings.json        # Generated Cursor config
└── README.md                # This documentation
```

### Development Installation

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# Install dependencies (now includes FastMCP 2.5+)
pip install -e .

# Test API
export YANGO_TECH_API_KEY="your_api_key"
python test_api_connection.py

# Run MCP server
python server.py
```

### Technology Stack

- **FastMCP 2.5+**: Modern MCP server framework
- **Python 3.8+**: Core language
- **HTTPx**: Async HTTP client
- **Pydantic**: Data validation
- **python-dotenv**: Environment management

### API Endpoints

Server works with real Yango Tech API:
- **Test URL**: `https://api.tst.eu.cloudretail.tech/b2b/v1`
- **Production URL**: `https://api.retailtech.yango.com/b2b/v1`
- **Authorization**: OAuth token in header
- **Methods**: POST for most requests
- **Pagination**: Cursor-based for large data

### IDE Support

- **Claude Desktop**: Uses `mcpServers` configuration
- **Cursor IDE**: Uses `mcp.servers` configuration
- **Auto-detection**: Installer detects which IDEs are installed
- **Universal**: Works without IDEs - configs always generated

</details>

---

## 📞 Support

If something doesn't work:

1. **Check Python**: `python3 --version` (should be 3.8+)
2. **Complete reset**: `python3 cleanup.py && python3 install.py`
3. **Manual setup**: Use generated config files (`claude_desktop_config.json`, `cursor_settings.json`)
4. **Manual setup guide**: [MANUAL_SETUP.md](MANUAL_SETUP.md) for detailed instructions
5. **Check IDE logs** (Claude Desktop or Cursor IDE)
6. **Make sure** IDEs are restarted after installation

---

**🎯 Goal: One command - and everything works in both Claude Desktop and Cursor IDE (or generates configs for manual setup)!**
