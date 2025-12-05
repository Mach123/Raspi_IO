#!/bin/bash
#
# NGP800 Control Setup Script for Raspberry Pi
# This script installs all necessary dependencies for controlling
# Rohde & Schwarz NGP800 power supply via PyVISA
#

set -e  # Exit on error

echo "============================================================"
echo "NGP800 Power Supply Control - Setup Script"
echo "============================================================"
echo ""

# Check if running on Raspberry Pi
if ! grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null && ! grep -q "BCM" /proc/cpuinfo 2>/dev/null; then
    echo "Warning: This doesn't appear to be a Raspberry Pi."
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Update package list
echo "Updating package list..."
sudo apt update

# Install Python3 and pip if not already installed
echo ""
echo "Checking Python3 installation..."
if ! command -v python3 &> /dev/null; then
    echo "Installing Python3..."
    sudo apt install -y python3
else
    echo "Python3 is already installed: $(python3 --version)"
fi

if ! command -v pip3 &> /dev/null; then
    echo "Installing pip3..."
    sudo apt install -y python3-pip
else
    echo "pip3 is already installed"
fi

# Install PyVISA and PyVISA-py
echo ""
echo "Installing PyVISA and PyVISA-py..."
pip3 install --user --upgrade pyvisa pyvisa-py

# Verify installation
echo ""
echo "Verifying installation..."
python3 -c "import pyvisa; print('PyVISA version:', pyvisa.__version__)" || {
    echo "Error: PyVISA installation failed"
    exit 1
}

# Make the control script executable
if [ -f "ngp800_control.py" ]; then
    chmod +x ngp800_control.py
    echo ""
    echo "Made ngp800_control.py executable"
fi

echo ""
echo "============================================================"
echo "Setup completed successfully!"
echo "============================================================"
echo ""
echo "Next steps:"
echo "1. Edit ngp800_control.py and set your NGP800's IP address"
echo "2. Ensure your NGP800 is connected to the network"
echo "3. Run the script with: python3 ngp800_control.py"
echo ""
echo "For more information, see NGP800_README.md"
echo ""
