# 🐍 Python Installation Guide

This guide helps you install Python if you don't have it or have an old version.

## 🔍 Check if You Have Python

First, check if Python is already installed:

**Open Terminal/Command Prompt and run:**
```bash
python3 --version
# or try
python --version
```

**Expected result:** `Python 3.8.0` or higher

If you see:
- `Python 2.x.x` - **Too old, need Python 3.8+**
- `command not found` - **Python not installed**
- `Python 3.7.x` or lower - **Too old for FastMCP**

---

## 📱 macOS Installation

### Option 1: Official Python (Recommended)
1. **Visit**: https://www.python.org/downloads/
2. **Download**: Latest Python 3.12+ for macOS
3. **Install**: Run the `.pkg` file and follow instructions
4. **Restart Terminal**
5. **Verify**: `python3 --version`

### Option 2: Homebrew
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.12

# Restart Terminal
python3 --version
```

### Option 3: pyenv (For Developers)
```bash
# Install pyenv
brew install pyenv

# Install latest Python
pyenv install 3.12.5
pyenv global 3.12.5

# Add to shell profile
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init --path)"' >> ~/.zshrc

# Restart Terminal
python3 --version
```

---

## 🪟 Windows Installation

### Option 1: Official Python (Recommended)
1. **Visit**: https://www.python.org/downloads/windows/
2. **Download**: Latest Python 3.12+ for Windows
3. **⚠️ IMPORTANT**: During installation, **check "Add Python to PATH"**
4. **Install**: Run the installer as Administrator
5. **Restart Command Prompt**
6. **Verify**: `python --version` or `python3 --version`

### Option 2: Microsoft Store
1. **Open**: Microsoft Store app
2. **Search**: "Python 3.12"
3. **Install**: Python from Microsoft Corporation
4. **Restart Command Prompt**
5. **Verify**: `python --version`

### Option 3: Chocolatey
```cmd
# Install Chocolatey first (Run as Administrator)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Python
choco install python

# Restart Command Prompt
python --version
```

---

## 🐧 Linux Installation

### Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Install Python 3.12
sudo apt install python3.12 python3.12-venv python3.12-pip

# Verify installation
python3.12 --version

# Make python3 point to 3.12 (optional)
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1
```

### CentOS/RHEL/Fedora
```bash
# For newer versions (Fedora/CentOS Stream)
sudo dnf install python3.12 python3.12-pip

# For older versions
sudo yum install python3.12 python3.12-pip

# Verify
python3.12 --version
```

### Arch Linux
```bash
# Install Python
sudo pacman -S python python-pip

# Verify
python --version
```

### From Source (Any Linux)
```bash
# Install build dependencies
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev

# Download Python source
wget https://www.python.org/ftp/python/3.12.5/Python-3.12.5.tgz
tar -xf Python-3.12.5.tgz
cd Python-3.12.5

# Configure and compile
./configure --enable-optimizations
make -j$(nproc)
sudo make altinstall

# Verify
python3.12 --version
```

---

## 🔧 Troubleshooting

### "Python not found" after installation

**Windows:**
1. Check PATH: `echo %PATH%` should include Python directory
2. Reinstall with "Add to PATH" checked
3. Restart Command Prompt as Administrator

**macOS/Linux:**
1. Check PATH: `echo $PATH` should include Python directory
2. Add to shell profile:
   ```bash
   echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

### "Permission denied" errors

**Solution**: Use `sudo` for system-wide installation:
```bash
sudo python3 -m pip install package_name
```

### Multiple Python versions conflict

**Use specific version:**
```bash
python3.12 install.py
# instead of
python3 install.py
```

### Python 2.x found instead of 3.x

**Check what `python` points to:**
```bash
which python
which python3

# Use python3 explicitly
python3 install.py
```

---

## ✅ Verify Installation

After installing Python, verify everything works:

```bash
# Check version
python3 --version

# Check pip
python3 -m pip --version

# Check virtual environment support
python3 -m venv test_env
rm -rf test_env  # Clean up test

# Everything good? Run the installer!
python3 install.py
```

---

## 🆘 Still Having Issues?

If Python installation fails:

1. **Try different installation method** from the options above
2. **Restart your terminal/computer** after installation
3. **Run as Administrator** (Windows) or with `sudo` (Linux/macOS)
4. **Check system requirements** - some very old systems may not support Python 3.8+
5. **Use manual setup** - see [MANUAL_SETUP.md](MANUAL_SETUP.md) for alternative installation methods

**For older systems:**
- Consider using Python 3.8 specifically if 3.12+ doesn't work
- Check if your OS is still supported by Python.org
- Consider upgrading your operating system

---

**🎯 Goal: Get Python 3.8+ working so you can run `python3 install.py`!** 