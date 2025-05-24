#!/usr/bin/env python3
"""
🧹 Complete cleanup script for Yango Tech MCP server
Removes all configurations, virtual environments, and cached files.

Usage: python3 cleanup.py
"""

import json
import os
import platform
import shutil
import sys
from pathlib import Path


def print_header():
    """Beautiful header."""
    print("=" * 60)
    print("🧹 YANGO TECH MCP SERVER CLEANUP")
    print("=" * 60)
    print()

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

def get_cursor_config_paths(os_type):
    """Get paths to Cursor IDE configuration."""
    if os_type == "macos":
        return [
            Path.home() / "Library" / "Application Support" / "Cursor" / "User" / "globalStorage" / "mcp.json",
            Path.home() / "Library" / "Application Support" / "Cursor" / "User" / "settings.json"
        ]
    elif os_type == "windows":
        appdata = Path(os.environ.get("APPDATA", ""))
        return [
            appdata / "Cursor" / "User" / "globalStorage" / "mcp.json",
            appdata / "Cursor" / "User" / "settings.json"
        ]
    elif os_type == "linux":
        return [
            Path.home() / ".config" / "Cursor" / "User" / "globalStorage" / "mcp.json",
            Path.home() / ".config" / "Cursor" / "User" / "settings.json"
        ]
    else:
        return []

def remove_virtual_environment(project_dir):
    """Remove virtual environment."""
    print_info("Removing virtual environment...")

    venv_dir = project_dir / ".venv"
    if venv_dir.exists():
        try:
            shutil.rmtree(venv_dir)
            print_success("Virtual environment removed")
        except Exception as e:
            print_error(f"Error removing virtual environment: {e}")
    else:
        print_info("Virtual environment not found")

def remove_env_files(project_dir):
    """Remove environment files."""
    print_info("Removing environment files...")

    env_files = [".env", ".env.local", ".env.development"]
    removed_count = 0

    for env_file in env_files:
        env_path = project_dir / env_file
        if env_path.exists():
            try:
                env_path.unlink()
                print_success(f"Removed {env_file}")
                removed_count += 1
            except Exception as e:
                print_error(f"Error removing {env_file}: {e}")

    if removed_count == 0:
        print_info("No environment files found")

def remove_claude_config(os_type):
    """Remove Yango Tech from Claude Desktop configuration."""
    print_info("Cleaning Claude Desktop configuration...")

    config_path = get_claude_config_path(os_type)
    if not config_path or not config_path.exists():
        print_info("Claude Desktop configuration not found")
        return

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # Remove yango-tech server
        if "mcpServers" in config and "yango-tech" in config["mcpServers"]:
            del config["mcpServers"]["yango-tech"]
            print_success("Removed yango-tech from Claude configuration")

            # If no servers left, remove mcpServers section
            if not config["mcpServers"]:
                del config["mcpServers"]

            # Write back configuration
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            print_success("Claude Desktop configuration updated")
        else:
            print_info("Yango Tech not found in Claude configuration")

    except json.JSONDecodeError:
        print_error("Invalid Claude configuration file")
    except Exception as e:
        print_error(f"Error updating Claude configuration: {e}")

def remove_cursor_config(os_type):
    """Remove Yango Tech from Cursor IDE configuration."""
    print_info("Cleaning Cursor IDE configuration...")

    config_paths = get_cursor_config_paths(os_type)
    found_config = False

    for config_path in config_paths:
        if not config_path.exists():
            continue

        found_config = True
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # Check for MCP configuration in different possible locations
            removed = False

            # Check in mcp.servers (newer format)
            if "mcp" in config and "servers" in config["mcp"]:
                if "yango-tech" in config["mcp"]["servers"]:
                    del config["mcp"]["servers"]["yango-tech"]
                    removed = True
                    if not config["mcp"]["servers"]:
                        del config["mcp"]["servers"]
                        if not config["mcp"]:
                            del config["mcp"]

            # Check in mcpServers (older format)
            if "mcpServers" in config and "yango-tech" in config["mcpServers"]:
                del config["mcpServers"]["yango-tech"]
                removed = True
                if not config["mcpServers"]:
                    del config["mcpServers"]

            if removed:
                # Write back configuration
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                print_success(f"Removed yango-tech from {config_path.name}")

        except json.JSONDecodeError:
            print_error(f"Invalid Cursor configuration file: {config_path}")
        except Exception as e:
            print_error(f"Error updating Cursor configuration {config_path}: {e}")

    if not found_config:
        print_info("Cursor IDE configuration not found")

def remove_cache_files(project_dir):
    """Remove cache and temporary files."""
    print_info("Removing cache files...")


    removed_count = 0

    # Remove __pycache__ directories
    for pycache_dir in project_dir.rglob("__pycache__"):
        try:
            shutil.rmtree(pycache_dir)
            removed_count += 1
        except Exception as e:
            print_error(f"Error removing {pycache_dir}: {e}")

    # Remove .pytest_cache
    pytest_cache = project_dir / ".pytest_cache"
    if pytest_cache.exists():
        try:
            shutil.rmtree(pytest_cache)
            removed_count += 1
        except Exception as e:
            print_error(f"Error removing .pytest_cache: {e}")

    # Remove .mypy_cache
    mypy_cache = project_dir / ".mypy_cache"
    if mypy_cache.exists():
        try:
            shutil.rmtree(mypy_cache)
            removed_count += 1
        except Exception as e:
            print_error(f"Error removing .mypy_cache: {e}")

    # Remove .ruff_cache
    ruff_cache = project_dir / ".ruff_cache"
    if ruff_cache.exists():
        try:
            shutil.rmtree(ruff_cache)
            removed_count += 1
        except Exception as e:
            print_error(f"Error removing .ruff_cache: {e}")

    # Remove egg-info directories
    for egg_info in project_dir.glob("*.egg-info"):
        try:
            if egg_info.is_dir():
                shutil.rmtree(egg_info)
            else:
                egg_info.unlink()
            removed_count += 1
        except Exception as e:
            print_error(f"Error removing {egg_info}: {e}")

    if removed_count > 0:
        print_success(f"Removed {removed_count} cache directories/files")
    else:
        print_info("No cache files found")

def remove_generated_config_files(project_dir):
    """Remove generated configuration files from project root."""
    print_info("Removing generated configuration files...")

    config_files = [
        "claude_desktop_config.json",
        "cursor_settings.json"
    ]

    removed_count = 0

    for config_file in config_files:
        config_path = project_dir / config_file
        if config_path.exists():
            try:
                config_path.unlink()
                print_success(f"Removed {config_file}")
                removed_count += 1
            except Exception as e:
                print_error(f"Error removing {config_file}: {e}")

    if removed_count == 0:
        print_info("No generated configuration files found")

def main():
    """Main cleanup function."""
    print_header()

    print("⚠️  WARNING: This will completely remove:")
    print("• Virtual environment (.venv)")
    print("• Environment files (.env)")
    print("• Yango Tech configuration from Claude Desktop")
    print("• Yango Tech configuration from Cursor IDE")
    print("• Generated configuration files (claude_desktop_config.json, cursor_settings.json)")
    print("• All cache files and directories")
    print()

    confirm = input("Are you sure you want to continue? (yes/no): ").strip().lower()
    if confirm not in ["yes", "y"]:
        print_info("Cleanup cancelled")
        return

    print()

    # Determine current project directory
    project_dir = Path(__file__).parent.absolute()
    print_info(f"Project folder: {project_dir}")

    # Determine OS
    os_type = get_os_info()
    print_info(f"Operating system: {os_type}")

    print()

    # Remove virtual environment
    remove_virtual_environment(project_dir)

    # Remove environment files
    remove_env_files(project_dir)

    # Remove Claude Desktop configuration
    remove_claude_config(os_type)

    # Remove Cursor IDE configuration
    remove_cursor_config(os_type)

    # Remove cache files
    remove_cache_files(project_dir)

    # Remove generated configuration files
    remove_generated_config_files(project_dir)

    print()
    print("🎉 CLEANUP COMPLETED!")
    print("=" * 60)
    print()
    print("✅ Environment completely cleaned")
    print("✅ All configurations removed")
    print("✅ Cache files deleted")
    print()
    print("📋 Next steps:")
    print("1. Run: python3 install.py")
    print("2. Restart Claude Desktop and/or Cursor IDE")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️  Cleanup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Critical error: {e}")
        sys.exit(1)
