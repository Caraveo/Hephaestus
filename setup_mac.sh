#!/bin/bash
# Setup script for Hephaestus on Mac
# This script helps resolve OpenMP conflicts

set -e

echo "Setting up Hephaestus environment for Mac..."

# Check if conda environment exists
if conda env list | grep -q "^hephaestus "; then
    echo "Environment 'hephaestus' already exists."
    read -p "Do you want to recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing existing environment..."
        conda env remove -n hephaestus -y
    else
        echo "Using existing environment. Activate it with: conda activate hephaestus"
        exit 0
    fi
fi

# Create environment
echo "Creating conda environment from environment_mac.yml..."
conda env create -f environment_mac.yml

# Activate and install additional fixes
echo "Activating environment and applying fixes..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate hephaestus

# Set environment variable to handle OpenMP conflicts
echo "Setting up OpenMP workaround..."
cat >> ~/.zshrc << 'EOF'

# Hephaestus OpenMP workaround
export KMP_DUPLICATE_LIB_OK=TRUE
EOF

# Also set for current session
export KMP_DUPLICATE_LIB_OK=TRUE

echo ""
echo "✓ Setup complete!"
echo ""
echo "The environment variable KMP_DUPLICATE_LIB_OK has been:"
echo "  1. Added to ~/.zshrc for future sessions"
echo "  2. Set in the current session"
echo ""
echo "Next steps:"
echo "  1. Activate the environment: conda activate hephaestus"
echo "  2. Test MPS: python test_mps.py"
echo "  3. Start generating: python -u sample_stage1.py --text 'a robot' --samples 1 --sampler ddim --steps 200 --cfg_scale 7.5 --seed 0"
echo ""
echo "Note: If you restart your terminal, the OpenMP fix will be automatically applied from ~/.zshrc"

