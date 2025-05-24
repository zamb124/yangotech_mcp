#!/usr/bin/env python3
"""
🚀 Universal installer for Yango Tech MCP server
Works on Mac and Windows. One command - and everything is ready!

Usage: python3 install.py
"""

import json
import os
import platform
import subprocess
import sys
from pathlib import Path


def print_header():
    """Beautiful header."""
    print("=" * 60)
    print("🚀 YANGO TECH MCP SERVER INSTALLATION")
    print("=" * 60)
    print()

def print_step(step, description):
    """Print current step."""
    print(f"📋 Step {step}: {description}")

def print_success(message):
    """Print success message."""
    print(f"✅ {message}")

def print_error(message):
    """Print error message."""
    print(f"❌ {message}")

def print_info(message):
    """Print informational message."""
    print(f"ℹ️  {message}")

def get_os_info():
    """Determine operating system."""
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    elif system == "windows":
        return "windows"
    elif system == "linux":
        return "linux"
    else:
        return "unknown"

def find_python():
    """Find Python interpreter and check version."""
    python_commands = ["python3", "python", "py"]

    print_info("Checking Python installation...")

    for cmd in python_commands:
        try:
            result = subprocess.run([cmd, "--version"],
                                  capture_output=True, text=True, check=True)

            # Parse version
            version_output = result.stdout.strip()
            if "Python" not in version_output:
                continue

            # Extract version numbers (e.g., "Python 3.9.7" -> "3.9.7")
            version_str = version_output.split("Python ")[1].split()[0]
            version_parts = version_str.split(".")

            try:
                major = int(version_parts[0])
                minor = int(version_parts[1]) if len(version_parts) > 1 else 0

                print_info(f"Found {version_output} via '{cmd}'")

                # Check version requirements
                if major < 3:
                    print_error(f"Python {major}.{minor} is too old. Python 3.8+ required.")
                    continue
                elif major == 3 and minor < 8:
                    print_error(f"Python 3.{minor} is too old. Python 3.8+ required for FastMCP.")
                    continue
                else:
                    print_success(f"Python {major}.{minor} meets requirements (3.8+)")
                    return cmd

            except (ValueError, IndexError):
                print_error(f"Could not parse Python version: {version_str}")
                continue

        except (subprocess.CalledProcessError, FileNotFoundError):
            continue

    return None

def show_python_installation_guide(os_type):
    """Show Python installation instructions for different operating systems."""
    print()
    print("=" * 60)
    print("🐍 PYTHON INSTALLATION REQUIRED")
    print("=" * 60)
    print()
    print("This installer requires Python 3.8 or newer.")
    print("Please install Python and try again.")
    print()

    if os_type == "macos":
        print("📱 macOS Installation Options:")
        print()
        print("Option 1: Official Python (Recommended)")
        print("1. Visit: https://www.python.org/downloads/")
        print("2. Download Python 3.12+ for macOS")
        print("3. Run the installer")
        print("4. Restart Terminal")
        print()
        print("Option 2: Homebrew")
        print("1. Install Homebrew: https://brew.sh")
        print("2. Run: brew install python@3.12")
        print("3. Restart Terminal")
        print()
        print("Option 3: pyenv (Advanced)")
        print("1. Install pyenv: brew install pyenv")
        print("2. Run: pyenv install 3.12.5")
        print("3. Run: pyenv global 3.12.5")

    elif os_type == "windows":
        print("🪟 Windows Installation Options:")
        print()
        print("Option 1: Official Python (Recommended)")
        print("1. Visit: https://www.python.org/downloads/windows/")
        print("2. Download Python 3.12+ for Windows")
        print("3. ⚠️  IMPORTANT: Check 'Add Python to PATH' during installation")
        print("4. Restart Command Prompt")
        print()
        print("Option 2: Microsoft Store")
        print("1. Open Microsoft Store")
        print("2. Search for 'Python 3.12'")
        print("3. Install Python from Microsoft")
        print("4. Restart Command Prompt")
        print()
        print("Option 3: Chocolatey")
        print("1. Install Chocolatey: https://chocolatey.org")
        print("2. Run: choco install python")
        print("3. Restart Command Prompt")

    elif os_type == "linux":
        print("🐧 Linux Installation Options:")
        print()
        print("Ubuntu/Debian:")
        print("sudo apt update")
        print("sudo apt install python3.12 python3.12-venv python3.12-pip")
        print()
        print("CentOS/RHEL/Fedora:")
        print("sudo dnf install python3.12 python3.12-pip")
        print("# or for older versions:")
        print("sudo yum install python3.12 python3.12-pip")
        print()
        print("Arch Linux:")
        print("sudo pacman -S python python-pip")
        print()
        print("From source (any Linux):")
        print("1. Download: https://www.python.org/downloads/source/")
        print("2. Extract and compile Python 3.12+")

    else:
        print("🌍 General Installation:")
        print("1. Visit: https://www.python.org/downloads/")
        print("2. Download Python 3.12+ for your system")
        print("3. Follow installation instructions")
        print("4. Make sure Python is added to PATH")

    print()
    print("🔍 Verify Installation:")
    print("After installation, run:")
    print("  python3 --version")
    print("  # or")
    print("  python --version")
    print()
    print("Expected output: Python 3.8.0 or higher")
    print()
    print("💡 Then run this installer again:")
    print("  python3 install.py")
    print()
    print("=" * 60)

def install_dependencies(python_cmd, project_dir):
    """Install dependencies."""
    print_step(2, "Creating virtual environment and installing dependencies")

    # Create virtual environment
    venv_dir = project_dir / ".venv"
    if not venv_dir.exists():
        print_info("Creating virtual environment...")
        result = subprocess.run([python_cmd, "-m", "venv", str(venv_dir)],
                               cwd=project_dir, capture_output=True, text=True)
        if result.returncode != 0:
            print_error(f"Error creating virtual environment: {result.stderr}")
            return False
        print_success("Virtual environment created")
    else:
        print_success("Virtual environment already exists")

    # Determine path to Python in virtual environment
    if get_os_info() == "windows":
        python_venv_path = venv_dir / "Scripts" / "python.exe"
    else:
        python_venv_path = venv_dir / "bin" / "python"

    # Install project and all dependencies (including FastMCP from pyproject.toml)
    print_info("Installing project and dependencies...")
    result = subprocess.run([str(python_venv_path), "-m", "pip", "install", "-e", "."],
                           cwd=project_dir, capture_output=True, text=True)
    if result.returncode != 0:
        print_error(f"Error installing project: {result.stderr}")
        return False

    print_success("All dependencies installed")
    return str(python_venv_path)

def get_claude_config_path(os_type):
    """Get path to Claude Desktop configuration."""
    if os_type == "macos":
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    elif os_type == "windows":
        return Path(os.environ.get("APPDATA", "")) / "Claude" / "claude_desktop_config.json"
    elif os_type == "linux":
        return Path.home() / ".config" / "Claude" / "claude_desktop_config.json"
    else:
        return None

def get_cursor_config_path(os_type):
    """Get path to Cursor IDE configuration."""
    if os_type == "macos":
        return Path.home() / "Library" / "Application Support" / "Cursor" / "User" / "settings.json"
    elif os_type == "windows":
        return Path(os.environ.get("APPDATA", "")) / "Cursor" / "User" / "settings.json"
    elif os_type == "linux":
        return Path.home() / ".config" / "Cursor" / "User" / "settings.json"
    else:
        return None

def check_ide_installations(os_type):
    """Check which IDEs are installed."""
    print_info("Checking installed IDEs...")

    installed_ides = []

    # Check Claude Desktop
    claude_path = get_claude_config_path(os_type)
    if claude_path and claude_path.parent.exists():
        installed_ides.append("Claude Desktop")
        print_success("Claude Desktop found")

    # Check Cursor IDE
    cursor_path = get_cursor_config_path(os_type)
    if cursor_path and cursor_path.parent.parent.exists():  # Check Cursor folder exists
        installed_ides.append("Cursor IDE")
        print_success("Cursor IDE found")

    if not installed_ides:
        print_info("No supported IDEs found")

    return installed_ides

def get_api_credentials():
    """Request API key and URL from user."""
    print()
    print("🔑 API Access Setup:")
    print("To work with Yango Tech API, you need an API key and server URL.")
    print()

    # Offer test settings
    print("Option 1: Use test settings (for demonstration)")
    print("Option 2: Enter your own settings")
    print()

    choice = input("Choose option (1 or 2): ").strip()

    if choice == "1":
        api_key = "SBW45ZNrp13OoU4Jps/GiAeFlJR4kB/8leInLS8DwZbYizPL2j2id44dRh/3mK7o5ouvLNE0ZWDqZ8xTP9FQ.DXFjZlsGtCKFIsncT4K6XlzUJJ+ewe7Xre50Yoksz2WSJ8YnaFc6Noqlqrn2GnKHy5Ptju3hsVcO18uFjrlrB4gPFvnpcFxQsni1WFds2quS8F08/Ezx8A8MwQt39WKRCwQ3wpMgwhVpzLrwDj65C/LozcH7fq22rg8opzZzjglc2ThJp4hnbhoYQyw44pp4g4WpKRNsquln7NoubRbeZOaAeaADiJppbn4GwP2OwewEijOgy9ROCW4SWw2lPPeaS7LPr4+j/Oofw7cokgZDXXG0b20b/drI3kdKx6vQx0C36JrM1ud8DnpGhxnCsFqfBu3vfeNXsOAeq+5DDrfITQ=="
        base_url = "https://api.tst.eu.cloudretail.tech"
        print_success("Using test settings")
        return api_key, base_url
    elif choice == "2":
        print()
        api_key = input("Enter your API key: ").strip()
        if not api_key:
            print_error("API key cannot be empty")
            return get_api_credentials()

        print()
        print("URL examples:")
        print("• Test: https://api.tst.eu.cloudretail.tech")
        print("• Production: https://api.retailtech.yango.com")
        print()
        base_url = input("Enter API server URL: ").strip()
        if not base_url:
            print_error("URL cannot be empty")
            return get_api_credentials()

        # Check URL format
        if not base_url.startswith(('http://', 'https://')):
            print_error("URL must start with http:// or https://")
            return get_api_credentials()

        print_success("Settings entered")
        return api_key, base_url
    else:
        print_error("Invalid choice. Please try again.")
        return get_api_credentials()

def create_env_file(project_dir, api_key, base_url):
    """Create .env file."""
    print_info("Creating .env file...")

    env_content = f"""YANGO_TECH_API_KEY={api_key}
YANGO_TECH_BASE_URL={base_url}
YANGO_TECH_TIMEOUT=30
YANGO_TECH_MAX_RETRIES=3
"""

    env_path = project_dir / ".env"
    try:
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print_success(f".env file created: {env_path}")
        return True
    except Exception as e:
        print_error(f"Error creating .env file: {e}")
        return False

def create_claude_config(project_dir, python_venv_path, api_key, base_url, os_type):
    """Create Claude Desktop configuration."""
    print_info("Creating Claude Desktop configuration...")

    config_path = get_claude_config_path(os_type)
    if not config_path:
        print_error("Unsupported operating system for Claude Desktop configuration")
        return False

    # Create configuration folder if not exists
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Use Python from virtual environment
    if os_type == "windows":
        python_command = str(project_dir / ".venv" / "Scripts" / "python.exe")
    else:
        python_command = str(project_dir / ".venv" / "bin" / "python")

    # Create configuration
    config = {
        "mcpServers": {
            "yango-tech": {
                "command": python_command,
                "args": [str(project_dir / "server.py")],
                "cwd": str(project_dir),
                "env": {
                    "YANGO_TECH_API_KEY": api_key,
                    "YANGO_TECH_BASE_URL": base_url,
                    "YANGO_TECH_TIMEOUT": "30",
                    "YANGO_TECH_MAX_RETRIES": "3"
                }
            }
        }
    }

    # Read existing configuration if exists
    existing_config = {}
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                existing_config = json.load(f)
        except json.JSONDecodeError:
            print_info("Existing Claude configuration file corrupted, creating new one")

    # Merge configurations
    if "mcpServers" not in existing_config:
        existing_config["mcpServers"] = {}

    existing_config["mcpServers"]["yango-tech"] = config["mcpServers"]["yango-tech"]

    # Write configuration
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(existing_config, f, indent=2, ensure_ascii=False)
        print_success(f"Claude Desktop configuration created: {config_path}")
        return True
    except Exception as e:
        print_error(f"Error writing Claude configuration: {e}")
        return False

def create_cursor_config(project_dir, python_venv_path, api_key, base_url, os_type):
    """Create Cursor IDE configuration."""
    print_info("Creating Cursor IDE configuration...")

    config_path = get_cursor_config_path(os_type)
    if not config_path:
        print_error("Unsupported operating system for Cursor IDE configuration")
        return False

    # Create configuration folder if not exists
    config_path.parent.mkdir(parents=True, exist_ok=True)

    # Use Python from virtual environment
    if os_type == "windows":
        python_command = str(project_dir / ".venv" / "Scripts" / "python.exe")
    else:
        python_command = str(project_dir / ".venv" / "bin" / "python")

    # Create MCP server configuration
    mcp_server_config = {
        "command": python_command,
        "args": [str(project_dir / "server.py")],
        "cwd": str(project_dir),
        "env": {
            "YANGO_TECH_API_KEY": api_key,
            "YANGO_TECH_BASE_URL": base_url,
            "YANGO_TECH_TIMEOUT": "30",
            "YANGO_TECH_MAX_RETRIES": "3"
        }
    }

    # Read existing configuration if exists
    existing_config = {}
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                existing_config = json.load(f)
        except json.JSONDecodeError:
            print_info("Existing Cursor configuration file corrupted, creating new one")

    # Ensure MCP configuration structure exists
    if "mcp" not in existing_config:
        existing_config["mcp"] = {}
    if "servers" not in existing_config["mcp"]:
        existing_config["mcp"]["servers"] = {}

    # Add Yango Tech server
    existing_config["mcp"]["servers"]["yango-tech"] = mcp_server_config

    # Write configuration
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(existing_config, f, indent=2, ensure_ascii=False)
        print_success(f"Cursor IDE configuration created: {config_path}")
        return True
    except Exception as e:
        print_error(f"Error writing Cursor configuration: {e}")
        return False

def generate_config_files(project_dir, python_venv_path, api_key, base_url, os_type):
    """Generate configuration files in project root for manual setup."""
    print_info("Generating configuration files in project root...")

    # Use Python from virtual environment
    if os_type == "windows":
        python_command = str(project_dir / ".venv" / "Scripts" / "python.exe")
    else:
        python_command = str(project_dir / ".venv" / "bin" / "python")

    # Claude Desktop configuration
    claude_config = {
        "mcpServers": {
            "yango-tech": {
                "command": python_command,
                "args": [str(project_dir / "server.py")],
                "cwd": str(project_dir),
                "env": {
                    "YANGO_TECH_API_KEY": api_key,
                    "YANGO_TECH_BASE_URL": base_url,
                    "YANGO_TECH_TIMEOUT": "30",
                    "YANGO_TECH_MAX_RETRIES": "3"
                }
            }
        }
    }

    # Cursor IDE configuration
    cursor_config = {
        "mcp": {
            "servers": {
                "yango-tech": {
                    "command": python_command,
                    "args": [str(project_dir / "server.py")],
                    "cwd": str(project_dir),
                    "env": {
                        "YANGO_TECH_API_KEY": api_key,
                        "YANGO_TECH_BASE_URL": base_url,
                        "YANGO_TECH_TIMEOUT": "30",
                        "YANGO_TECH_MAX_RETRIES": "3"
                    }
                }
            }
        }
    }

    try:
        # Save Claude Desktop config
        claude_config_path = project_dir / "claude_desktop_config.json"
        with open(claude_config_path, 'w', encoding='utf-8') as f:
            json.dump(claude_config, f, indent=2, ensure_ascii=False)
        print_success(f"Claude Desktop config saved: {claude_config_path}")

        # Save Cursor IDE config
        cursor_config_path = project_dir / "cursor_settings.json"
        with open(cursor_config_path, 'w', encoding='utf-8') as f:
            json.dump(cursor_config, f, indent=2, ensure_ascii=False)
        print_success(f"Cursor IDE config saved: {cursor_config_path}")

        return True
    except Exception as e:
        print_error(f"Error generating config files: {e}")
        return False

def test_installation(python_venv_path, project_dir, api_key, base_url):
    """Test installation."""

    # Create test script
    test_script = f'''
import sys
import os
sys.path.insert(0, "{project_dir}")

os.environ["YANGO_TECH_API_KEY"] = "{api_key}"
os.environ["YANGO_TECH_BASE_URL"] = "{base_url}"
os.environ["YANGO_TECH_TIMEOUT"] = "10"
os.environ["YANGO_TECH_MAX_RETRIES"] = "1"

try:
    from client import YangoTechClient, YangoTechAPIError
    from models import AuthConfig

    # Simple configuration test
    config = AuthConfig(
        api_key=os.environ["YANGO_TECH_API_KEY"],
        base_url=os.environ["YANGO_TECH_BASE_URL"],
        timeout=10,
        max_retries=1
    )

    # Create client instance to verify configuration works
    client = YangoTechClient(config)
    print("✅ All modules loaded correctly")
    print("✅ Client configuration created successfully")

except Exception as e:
    print(f"❌ Test error: {{e}}")
    sys.exit(1)
'''

    # Run test
    result = subprocess.run([str(python_venv_path), "-c", test_script],
                           cwd=project_dir, capture_output=True, text=True)

    if result.returncode == 0:
        print(result.stdout)
        return True
    else:
        print_error(f"Test error: {result.stderr}")
        return False

def main():
    """Main installation function."""
    print_header()

    # Determine current project directory
    project_dir = Path(__file__).parent.absolute()
    print_info(f"Project folder: {project_dir}")

    # Determine OS
    os_type = get_os_info()
    print_info(f"Operating system: {os_type}")

    # Check installed IDEs
    installed_ides = check_ide_installations(os_type)

    # Find Python
    print_step(1, "Finding Python interpreter")
    python_cmd = find_python()
    if not python_cmd:
        show_python_installation_guide(os_type)
        sys.exit(1)
    print_success(f"Found Python: {python_cmd}")

    # Install dependencies
    python_venv_path = install_dependencies(python_cmd, project_dir)
    if not python_venv_path:
        print_error("Error installing dependencies")
        print_info("Use manual setup in MANUAL_SETUP.md")
        sys.exit(1)

    # Get API settings
    print_step(3, "API access setup")
    api_key, base_url = get_api_credentials()
    print_success("API settings saved")

    # Create .env file
    if not create_env_file(project_dir, api_key, base_url):
        print_error("Error creating .env file")
        sys.exit(1)

    # Create configurations for installed IDEs
    print_step(4, "Creating IDE configurations")

    configs_created = []
    configs_attempted = []

    # Create Claude Desktop configuration if installed
    if "Claude Desktop" in installed_ides:
        configs_attempted.append("Claude Desktop")
        if create_claude_config(project_dir, python_venv_path, api_key, base_url, os_type):
            configs_created.append("Claude Desktop")
        else:
            print_error("Error creating Claude Desktop configuration")

    # Create Cursor IDE configuration if installed
    if "Cursor IDE" in installed_ides:
        configs_attempted.append("Cursor IDE")
        if create_cursor_config(project_dir, python_venv_path, api_key, base_url, os_type):
            configs_created.append("Cursor IDE")
        else:
            print_error("Error creating Cursor IDE configuration")

    # Always generate configuration files in project root
    print_step(5, "Generating configuration files")
    if generate_config_files(project_dir, python_venv_path, api_key, base_url, os_type):
        print_success("Configuration files generated in project root")
    else:
        print_error("Error generating configuration files")

    # Summary of what was configured
    if configs_created:
        print_success(f"Direct IDE configurations created for: {', '.join(configs_created)}")

    if not installed_ides:
        print_info("No IDEs detected. Configuration files saved in project root for manual setup.")
    elif not configs_created:
        print_info("IDE configurations failed. Use manual setup with generated files.")

    # Testing
    print_step(6, "Testing installation")
    if not test_installation(python_venv_path, project_dir, api_key, base_url):
        print_error("Error testing installation")
        print_info("Check settings manually using generated configuration files")

    # Final instructions
    print()
    print("🎉 INSTALLATION COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print()

    if configs_created or not installed_ides:
        print("📋 What's next:")
        step_num = 1

        if "Claude Desktop" in configs_created:
            print(f"{step_num}. Restart Claude Desktop")
            step_num += 1
        if "Cursor IDE" in configs_created:
            print(f"{step_num}. Restart Cursor IDE")
            step_num += 1

        if not installed_ides:
            print(f"{step_num}. Install Claude Desktop or Cursor IDE")
            print(f"{step_num + 1}. Use generated configuration files for manual setup")
            step_num += 2

        print(f"{step_num}. You should see 6 Yango Tech tools")
        print(f"{step_num + 1}. Test: 'Get product information'")

    print()
    print("🧪 Test commands:")
    print("• 'Show status of order 240920-728268'")
    print("• 'What about order 240920-728268?'")
    print("• 'Show 5 products from catalog'")
    print("• 'Show product stocks in stores'")

    print()
    print("📁 Generated configuration files:")
    print(f"   Claude Desktop: {project_dir}/claude_desktop_config.json")
    print(f"   Cursor IDE: {project_dir}/cursor_settings.json")
    print()

    if configs_created:
        print("📁 Active configurations:")
        if "Claude Desktop" in configs_created:
            print(f"   Claude Desktop: {get_claude_config_path(os_type)}")
        if "Cursor IDE" in configs_created:
            print(f"   Cursor IDE: {get_cursor_config_path(os_type)}")
        print()

    if not installed_ides:
        print("💡 Next steps for manual setup:")
        print("1. Install Claude Desktop and/or Cursor IDE")
        print("2. Copy contents from generated config files to IDE settings")
        print("3. See MANUAL_SETUP.md for detailed instructions")
        print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️  Installation interrupted by user")
        print()
        print("📖 For manual setup use: MANUAL_SETUP.md")
        sys.exit(1)
    except Exception as e:
        print_error(f"Critical error: {e}")
        print()
        print("📖 If installer doesn't work, use manual setup instructions:")
        print("   👉 Open MANUAL_SETUP.md file")
        print("   👉 It contains detailed instructions for Claude Desktop and Cursor IDE")
        sys.exit(1)
